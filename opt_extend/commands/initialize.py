"""The initialize command."""
import os
import json

from .base import *
from .common import formatters


class Initialize(Base):
  """
  Initialize the files necessary to generate an Extension, in the specified directory

  Usage:
    opt-extend initialize <project_id> <directory_path> <edit_url> [--description=<description>] [--name=<name>]
  """

  async def run(self):
    extension_name = self.options.get('--name')
    project_id = self.options.get('<project_id>')
    edit_url = self.options.get('<edit_url>')
    description = self.options.get('--description')
    path_to_directory = self.options.get('<directory_path>')

    initialize_extension_files(path_to_directory, extension_name, project_id, edit_url, description)
    print('Initialized directory {} to contain {}'.format(path_to_directory, extension_name))


def initialize_extension_files(path_to_directory, name, project_id, edit_url, description=None):
  """
  Creates:
   - apply_js.js: JS to apply the Extension
   - reset_js.js: JS to cleanup the Extension
   - extension.html: HTML template for the Extension
   - extension.css: CSS to apply to the Extension
   - editable_fields.json: JSON dict of editable fields, see https://developers.optimizely.com/x/extensions/#fields
   - config.json: holds the high-level Extension data like name, description, etc.
   """
  files_to_create = ['apply_js.js', 'reset_js.js', 'extension.html', 'extension.css']

  if not os.path.isdir(os.path.expanduser(path_to_directory)):
    os.makedirs(os.path.expanduser(path_to_directory))

  for filename in files_to_create:
    full_path = formatters.generate_file_path(path_to_directory, filename)
    # Append so we don't overwrite if they already exist
    open(full_path, 'w').close()

  extension_config = {
    'name': name,
    'description': description,
    'project_id': project_id,
    'edit_url': edit_url
  }
  config_path = path_to_directory.rstrip('/') + '/config.json'
  with open(config_path, 'w') as config_file:
    json.dump(extension_config, config_file)

  editable_fields_path = path_to_directory.rstrip('/') + 'editable_fields.json'
  with open(editable_fields_path, 'w') as editable_fields:
    json.dump([{
            'api_name': 'text',
            'label': 'A text field',
            'default_value': 'My Butterbar',
            'field_type': 'text'
        }], editable_fields)
