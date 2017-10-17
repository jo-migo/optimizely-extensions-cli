"The upload command. Either creates a new Extension in Optimizely or updates the existing one"
import json
import os
import sys

from .common import authorization
from .common import formatters
from .base import *


class Upload(Base):
    """
  Upload an Extension to the current project

  If there is an ID in config.json, the extension with that ID will updated.
  If there is no ID in config.json, a new extension will be created in the specified project

  Usage:
      opt-extend upload <extension_directory_path> [--enable]
  """

    async def run(self):
        directory_path = self.options.get('<extension_directory_path>')
        project_id = get_project_id_from_config(directory_path)
        self.auth_options = authorization.get_token_for_project(project_id)
        enable = self.options.get('--enable')
        import pdb; pdb.set_trace()
        extension_data, extension_config = generate_extension_data_from_directory(directory_path, enable=enable)
        self.push_extension(extension_data, directory_path, extension_config)

    def push_extension(self, extension_data, directory_path, extension_config):
        # This Extension is already linked to an Optimizely Extension, so update it.
        if 'id' in extension_data:
            self.client.Extensions.update_extension(extension_id=extension_data['id'],
                                                    body=extension_data,
                                                    _request_options={"headers": self.auth_options})
            print('Successfully updated Extension {}'.format(extension_data['id']))
        # This Extension has not yet been pushed to Optimizely, so create it and store its ID.
        else:
            request = self.client.Extensions.create_extension(body=extension_data,
                                                              _request_options={"headers": self.auth_options})
            new_extension, http_resp = request.result()
            if new_extension['id']:
                with open(formatters.generate_file_path(directory_path, 'config.json'), 'w') as config_file:
                    extension_config['id'] = new_extension['id']
                    json.dump(extension_config, config_file)
            print('Successfully created new Extension {}'.format(extension_config['id']))

def get_project_id_from_config(directory_path):
    if not os.path.isdir(directory_path):
        print('Invalid extension directory-- config.json required: {}'.format(directory_path))
        sys.exit(1)
    with open(formatters.generate_file_path(directory_path, 'config.json')) as config_file:
        extension_config = json.load(config_file)
    return extension_config.get('project_id')

def generate_extension_data_from_directory(directory_path, enable=False):
    """
  Uses these within directory_path dir to build the extension and either update or create it in Optimizely
   apply_js., reset_js.js, extension.html, editable_fields.json, config.json
  """
    need_files = ['config.json', 'apply_js.js', 'reset_js.js', 'extension.css', 'extension.html',
                  'editable_fields.json']
    if not os.path.isdir(directory_path):
        print('Invalid extension directory: {}'.format(directory_path))
        sys.exit()
    if any([not os.path.exists(formatters.generate_file_path(directory_path, filename)) for filename in need_files]):
        necessary_files = '\n'.join(need_files)
        print('Incorrectly configured extension directory. Required files: \n{}'.format(necessary_files))
        sys.exit()

    with open(formatters.generate_file_path(directory_path, 'config.json')) as config_file:
        extension_config = json.load(config_file)

    extension_data = extension_config.copy()
    implementation = {}
    with open(formatters.generate_file_path(directory_path, 'apply_js.js')) as apply_js:
        implementation['apply_js'] = apply_js.read()

    with open(formatters.generate_file_path(directory_path, 'reset_js.js')) as reset_js:
        implementation['reset_js'] = reset_js.read()

    with open(formatters.generate_file_path(directory_path, 'extension.html')) as extension_html:
        implementation['html'] = extension_html.read()

    with open(formatters.generate_file_path(directory_path, 'extension.css')) as extension_css:
        implementation['css'] = extension_css.read()

    extension_data['implementation'] = implementation

    with open(formatters.generate_file_path(directory_path, 'editable_fields.json')) as editable_fields:
        editable_fields = json.load(editable_fields)

    extension_data['fields'] = editable_fields

    if enable:
        extension_data['enabled'] = True

    return extension_data, extension_config
