"The batch update command. Either creates a new Extension in Optimizely or updates the existing one"
import asyncio
import aiohttp
import json
import os
import sys
from .base import *

from .common import authorization
from .common import formatters
from .common import getters


BASE_PATCH_URL = swagger_client.OPTIMIZELY_BASE_URL + 'extensions/{}'
IMPLEMENTATION_FIELD_TO_FILE = {
  'apply_js': 'apply_js.js',
  'reset_js': 'reset_js.js',
  'html': 'extension.html',
  'css': 'extension.css'
}

class Update(Base):
  """
  Make a (batch) update to Extensions in a project. These Extension updates are limited to any CSS/JS/HTML
  implementation change or a change to editable fields.

  Usage:

    opt-extend update <project_id> (--all | --grep=<grep_string> | --extension-id=<extension_id>) (--css-only=<css_file> | <update_directory>)
  """

  async def run(self):
    project_id = self.options.get('<project_id>')
    self.auth_options = authorization.get_token_for_project(project_id)
    extensions_to_update = self.get_extensions_to_update(project_id)
    request_body = self.generate_update_body()
    if not request_body:
      print('Invalid CSS or update directory-- no request body generated.')
      sys.exit(1)
    await self.dispatch_requests(extensions_to_update, request_body)

  def get_extensions_to_update(self, project_id):
    if self.options.get('--all') or self.options.get('--grep'):
      if self.options.get('--all'):
        extensions = getters.get_all_extensions_in_project(project_id, self.auth_options)
      else:
        extensions = getters.get_all_extensions_in_project(project_id, self.auth_options,
                                                           getters.contains_grep_string,
                                                           grep_string=self.options.get('--grep'))
    else:
      extension_id = self.options.get('--extension_id')
      req = self.client.Extensions.get_extension(extension_id, _request_options=self.auth_options)
      extension, http_resp = req.result()
      extensions = [extension]
    return extensions

  def generate_update_body(self):
    extension_data = {}
    css_file = self.options.get('--css-only')
    if not css_file:
      directory_path = self.options.get('<update_directory>')

      extension_files = ['apply_js.js', 'reset_js.js', 'extension.css', 'extension.html']
      exists = list(filter(lambda f: os.path.exists(formatters.generate_file_path(directory_path, f)), extension_files))

      implementation = {}
      for implementation_field in IMPLEMENTATION_FIELD_TO_FILE:
        fname = IMPLEMENTATION_FIELD_TO_FILE[implementation_field]
        if fname in exists:
          with open(formatters.generate_file_path(directory_path, fname), 'r') as implementation_file:
              implementation[implementation_field] = implementation_file.read()

      extension_data['implementation'] = implementation
      if os.path.exists(formatters.generate_file_path(directory_path, 'editable_fields.json')):
        with open(formatters.generate_file_path(directory_path, 'editable_fields.json')) as editable_fields:
          editable_fields = json.load(editable_fields)
          extension_data['fields'] = editable_fields

    else:
      with open(os.path.expanduser(css_file), 'r') as css_file:
        extension_data['implementation'] = {'css': css_file.read()}

    return extension_data

  async def do_patch(self, url, session, formdata):
      async with session.patch(url, data=json.dumps(formdata), headers=self.auth_options) as response:
          return await response.json()

  async def dispatch_requests(self, extensions_to_update, request_body):
    tasks = []

    async with aiohttp.ClientSession() as session:
      for extension in extensions_to_update:
        extension_update = insert_updates(extension, request_body)
        task = asyncio.ensure_future(self.do_patch(BASE_PATCH_URL.format(extension['id']), session, extension_update))
        tasks.append(task)

      responses = await asyncio.gather(*tasks)

      for extension_response in responses:
        extension_body = extension_response
        if extension_body.get('id'):
          print('Updated Extension {}: {}'.format(extension_body['id'], extension_body['name']))
        else:
          print(extension_body)

def insert_updates(extension, request_body):
  extension_update = {}
  if 'implementation' in request_body:
    new_implementation = {
      'apply_js': request_body['implementation'].get('apply_js') or extension['implementation'].apply_js,
      'reset_js': request_body['implementation'].get('reset_js') or extension['implementation'].reset_js,
      'css': request_body['implementation'].get('css') or extension['implementation'].css,
      'html': request_body['implementation'].get('apply_js') or extension['implementation'].html
    }
    extension_update['implementation'] = new_implementation
  if 'fields' in request_body:
    extension_update['fields'] = request_body['fields']
  return extension_update
