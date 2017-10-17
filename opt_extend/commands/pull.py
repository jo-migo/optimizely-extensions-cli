"""The pull command (pulls an Extension from Optimizely into the specified directory)"""
import json
import os

from .common import authorization
from .common import formatters
from .base import *

IMPLEMENTATION_FILES = {
  'apply_js.js': 'apply_js',
  'reset_js.js': 'reset_js',
  'extension.html': 'html',
  'extension.css': 'css'
}


class Pull(Base):
  """
  Pull an Optimizely Extension into the designated directory for local development

  Usage:
    opt-extend pull <extension_id> <extension_directory_path>
  """

  async def run(self):
    extension_id = self.options.get('<extension_id>')
    project_id = self.options.get('<project_id>')
    self.auth_options = authorization.get_token_for_project(project_id)
    destination_directory = self.options.get('<extension_directory_path>')
    self.load_extension_into_directory(extension_id, destination_directory)


  def load_extension_into_directory(self, extension_id, destination_directory):
    extension = self.client.Extensions.get_extension(extension_id=extension_id,
                                                     _request_options={"headers": self.auth_options})
    extension, http_resp = extension.result()
    if not os.path.isdir(destination_directory):
      os.makedirs(destination_directory)

    for file_name in IMPLEMENTATION_FILES:
      file_path = formatters.generate_file_path(destination_directory, file_name)
      with open(file_path, 'w') as implementation_file:
        implementation_file.write(extension['implementation'][IMPLEMENTATION_FILES[file_name]])

    extension_config = {
      'name': extension['name'],
      'id': extension['id'],
      'description': extension['description'],
      'project_id': extension['project_id'],
      'edit_url': extension['edit_url']
    }

    config_path = destination_directory.rstrip('/') + '/config.json'
    with open(config_path, 'w') as config_file:
      json.dump(extension_config, config_file)

    fields_json = []
    for field in extension['fields']:
      fields_json.append(
        {
          'api_name': field.api_name,
          'label': field.label,
          'default_value': field.default_value,
          'field_type': field.field_type,
          'options': formatters.expand_options(field.options)
        }
      )

    editable_fields_path = formatters.generate_file_path(destination_directory, 'editable_fields.json')
    with open(editable_fields_path, 'w') as editable_fields:
      json.dump(fields_json, editable_fields)
