"""Input for Apps"""
# standard library
import json
import logging
import os
import re
from base64 import b64decode
from pathlib import Path
from typing import Dict, Optional, Union

# third-party
from pydantic import BaseModel, Extra

# first-party
from tcex.app_config.install_json import InstallJson
from tcex.backports import cached_property
from tcex.input.field_types import Sensitive
from tcex.input.models import feature_map, runtime_level_map
from tcex.playbook import Playbook
from tcex.pleb import Event, NoneModel, proxies
from tcex.registry import service_registry
from tcex.sessions import TcSession
from tcex.utils import Utils

# get tcex logger
logger = logging.getLogger('tcex')

# define JSON encoders
json_encoders = {Sensitive: lambda v: str(v)}  # pylint: disable=W0108


def input_model(models: list) -> BaseModel:
    """Return Input Model."""

    class InputModel(*models):
        """Input Model"""

        # [legacy] if True, the App should get it's inputs from secure params (redis)
        # supported runtimeLevel: [Organization, Playbook]
        tc_secure_params: bool = False

        # the user id of the one executing the App
        # supported runtimeLevel: [Organization, Playbook]
        tc_user_id: Optional[int]

        class Config:
            """DataModel Config"""

            extra = Extra.allow
            validate_assignment = True
            json_encoders = json_encoders

    return InputModel


class Input:
    """Module to handle inputs for all App types."""

    def __init__(self, config: Optional[dict] = None, config_file: Optional[str] = None) -> None:
        """Initialize class properties."""
        self.config = config
        self.config_file = config_file

        # properties
        self._models = []
        self.event = Event()
        self.ij = InstallJson()
        self.log = logger
        self.utils = Utils()
        self.variable_pattern = re.compile(r'&\{(?P<provider>\w+):(?P<type>\w+):(?P<key>.*)\}')

    def _load_aot_params(
        self,
        tc_aot_enabled: bool,
        tc_kvstore_type: str,
        tc_kvstore_host: str,
        tc_kvstore_port: int,
        tc_action_channel: str,
        tc_terminate_seconds: int,
    ) -> Dict[str, any]:
        """Subscribe to AOT action channel."""
        params = {}
        if tc_aot_enabled is not True:
            return params

        if tc_kvstore_type == 'Redis':

            # get an instance of redis client
            redis_client = RedisClient(
                host=tc_kvstore_host,
                port=tc_kvstore_port,
                db=0,
            ).client

            try:
                self.log.info('feature=inputs, event=blocking-for-aot')
                msg_data = redis_client.blpop(
                    keys=tc_action_channel,
                    timeout=tc_terminate_seconds,
                )

                if msg_data is None:  # pragma: no cover
                    # send exit to tcex.exit method
                    self.event.send('exit', code=1, msg='AOT subscription timeout reached.')

                msg_data = json.loads(msg_data[1])
                msg_type = msg_data.get('type', 'terminate')
                if msg_type == 'execute':
                    params = msg_data.get('params', {})
                elif msg_type == 'terminate':
                    # send exit to tcex.exit method
                    self.event.send('exit', code=0, msg='Received AOT terminate message.')
            except Exception as e:  # pragma: no cover
                # send exit to tcex.exit method
                self.event.send('exit', code=1, msg=f'Exception during AOT subscription ({e}).')

        return params

    def _load_config_file(self):
        """Load config file params provided passed to inputs."""
        # default file contents
        file_content = {}
        if self.config_file is None:
            return file_content

        # self.config_file should be a fully qualified file name
        fqfn = Path(self.config_file)
        if not fqfn.is_file():
            self.log.error(
                'feature=inputs, event=load-config-file, '
                f'exception=file-not-found, filename={fqfn.name}'
            )
            return file_content

        # read file contents
        try:
            # read encrypted file from "in" directory
            with fqfn.open(mode='rb') as fh:
                return json.load(fh)
        except Exception:  # pragma: no cover
            self.log.error(f'feature=inputs, event=config-parse-failure, filename={fqfn.name}')
            return file_content

    def _load_file_params(self):
        """Load file params provided by the core platform."""
        # default file contents
        file_content = {}

        tc_app_param_file = os.getenv('TC_APP_PARAM_FILE')
        tc_app_param_key = os.getenv('TC_APP_PARAM_KEY')
        if not all([tc_app_param_file, tc_app_param_key]):
            return file_content

        # tc_app_param_file is a fully qualified file name
        fqfn = Path(tc_app_param_file)
        if not fqfn.is_file():
            self.log.error(
                'feature=inputs, event=load-file-params, '
                f'exception=file-not-found, filename={fqfn.name}'
            )
            return file_content

        # read file contents
        try:
            # read encrypted file from "in" directory
            with fqfn.open(mode='rb') as fh:
                encrypted_contents = fh.read()
        except Exception:  # pragma: no cover
            self.log.error(f'feature=inputs, event=config-parse-failure, filename={fqfn.name}')
            return file_content

        # decrypt file contents
        try:
            file_content = json.loads(
                self.utils.decrypt_aes_cbc(tc_app_param_key, encrypted_contents).decode()
            )

            # delete file
            fqfn.unlink()
        except Exception:  # pragma: no cover
            self.log.error(f'feature=inputs, event=config-decryption-failure, filename={fqfn.name}')

        return file_content

    def _resolve_variable(self, provider: str, key: str, type_: str) -> Union[bytes, str]:
        """Resolve TEXT/KEYCHAIN/FILE variables.

        Feature: PLAT-2688

        Data Format:
        {
            "data": "value"
        }
        """
        data = None

        # retrieve value from API
        r = service_registry.session_tc.get(f'/internal/variable/runtime/{provider}/{key}')
        if r.ok:
            try:
                data = r.json().get('data')

                if type_.lower() == 'file':
                    data = b64decode(data)  # returns bytes
                elif type_.lower() == 'keychain':
                    # TODO: [high] will the developer know this is sensitive
                    #              and access the "value" property
                    data = Sensitive(data)
            except Exception as ex:
                raise RuntimeError(
                    f'Could not retrieve variable: provider={provider}, key={key}, type={type_}.'
                ) from ex
        else:
            raise RuntimeError(
                f'Could not retrieve variable: provider={provider}, key={key}, type={type_}.'
            )

        return data

    def add_model(self, model: BaseModel) -> None:
        """Add additional input models."""
        # TODO: [high] @paco - for some custom defined field types we need to make API calls
        #       (e.g., indicator types). In order to do this we need a session object in
        #       the custom field types, so we use a singleton Session object that needs
        #       to get instantiated before the datamodel parses the App inputs, but after
        #       the "base" inputs are loaded into the model.
        _ = service_registry.session_tc

        if model:
            self._models.insert(0, model)

        # clear cache for data property
        if 'data' in self.__dict__:
            del self.__dict__['data']

        # force data model to load so that validation is done at this EXACT point
        _ = self.data

    @cached_property
    def contents(self) -> dict:
        """Return contents of inputs from all locations."""
        _contents = {}

        # config
        if isinstance(self.config, dict):
            _contents.update(self.config)

        # config file
        _contents.update(self._load_config_file())

        # file params
        _contents.update(self._load_file_params())

        # aot params
        _contents.update(
            self._load_aot_params(
                tc_aot_enabled=_contents.get('tc_aot_enabled', False),
                tc_kvstore_type=_contents.get('tc_kvstore_type'),
                tc_kvstore_host=_contents.get('tc_kvstore_host'),
                tc_kvstore_port=_contents.get('tc_kvstore_port'),
                tc_action_channel=_contents.get('tc_action_channel'),
                tc_terminate_seconds=_contents.get('tc_terminate_seconds'),
            )
        )

        return _contents

    @cached_property
    def contents_resolved(self) -> dict:
        """Resolve all file, keychain, playbook, and text variables."""
        _inputs = self.contents

        # support external Apps that don't have an install.json
        if not self.ij.fqfn.is_file():
            return _inputs

        for name, value in _inputs.items():
            # model properties at this point are the default fields passed by ThreatConnect
            # these should not be playbook variables and will not need to be resolved.
            if name in self.model_properties:
                continue

            if isinstance(value, list):
                # TODO: [low] are playbooks the only App type that can get a list?
                #             is this condition needed?
                if self.ij.data.runtime_level.lower() == 'playbook':
                    # list could contain variables, try to resolve the value
                    updated_value_array = []
                    for v in value:
                        if isinstance(v, str):
                            v = self.playbook.read(v)
                        updated_value_array.append(v)
                    _inputs[name] = updated_value_array
            elif isinstance(value, str):
                # strings could be a variable, try to resolve the value
                if self.variable_pattern.match(value):
                    m = self.variable_pattern.search(value)
                    if not any(
                        [
                            m.group('provider'),
                            m.group('key'),
                            m.group('type'),
                        ]
                    ):
                        # TODO: [med] should this an exit
                        raise RuntimeError(f'Could not parse variable {value}.')

                    _inputs[name] = self._resolve_variable(
                        m.group('provider'), m.group('key'), m.group('type')
                    )
                    # _inputs[name] = self._resolve_variable(**m.groupdict())
                elif self.ij.data.runtime_level.lower() == 'playbook':
                    _inputs[name] = self.playbook.read(value)

        # update contents
        self.contents_update(_inputs)

        return dict(sorted(_inputs.items()))

    # TODO: [high] - can this be replaced with a pydantic root validator?
    def contents_update(self, inputs: dict) -> None:
        """Update inputs provided by AOT to be of the proper value and type."""
        for name, value in inputs.items():
            # model properties at this point are the default fields passed by ThreatConnect
            # these should not be playbook variables and will not need to be resolved.
            if name in self.model_properties:
                continue

            # ThreatConnect AOT params could be updated in the future to proper JSON format.
            # MultiChoice data should be represented as JSON array and Boolean values should be a
            # JSON boolean and not a string.
            param = self.ij.data.get_param(name)
            if isinstance(param, NoneModel):
                # skip over "default" inputs not defined in the install.json file
                continue

            if param.type.lower() == 'multichoice' or param.allow_multiple:
                # update delimited value to an array for inputs that have type of MultiChoice
                if value is not None and not isinstance(value, list):
                    inputs[name] = value.split(self.ij.data.list_delimiter or '|')
            elif param.type == 'boolean' and isinstance(value, str):
                # convert boolean input that are passed in as a string ("true" -> True)
                inputs[name] = str(value).lower() == 'true'

    @cached_property
    def data(self) -> BaseModel:
        """Return the Input Model."""
        return input_model(self.models)(**self.contents_resolved)

    @cached_property
    def data_unresolved(self) -> BaseModel:
        """Return the Input Model using contents (no resolved values)."""
        return input_model(self.models)(**self.contents)

    @cached_property
    def models(self) -> list:
        """Return all models for inputs."""
        # support external Apps that don't have an install.json
        if not self.ij.fqfn.is_file():
            return runtime_level_map.get('external')

        # add all models for any supported features of the App
        for feature in self.ij.data.features:
            self._models.extend(feature_map.get(feature))

        # add all models based on the runtime level of the App
        self._models.extend(runtime_level_map.get(self.ij.data.runtime_level.lower()))

        return self._models

    # TODO: [low] is this needed or can Field value be set to tc_property=True?
    @cached_property
    def model_properties(self) -> set:
        """Return only defined properties from model (exclude additional)."""
        properties = set()
        for model in self.models:
            properties.update(model.schema().get('properties').keys())

        return properties
