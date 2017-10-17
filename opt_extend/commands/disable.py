"""The batch disable command.
"""
import asyncio
import aiohttp
import json

from .base import *

from .common import authorization
from .common import getters
from .common import swagger_client

BASE_PATCH_URL = swagger_client.OPTIMIZELY_BASE_URL + "extensions/{}"

class Disable(Base):
  """
  opt-extend disable <project_id> (--grep=<grep_string> | --extension-id=<extension_id>)
  """
  async def run(self):
    project_id = self.options.get('<project_id>')
    self.auth_options = authorization.get_token_for_project(project_id)
    extension_id = self.options.get('--extension-id')
    grep_string = self.options.get('--grep')

    if grep_string:
      extensions = await self.get_extensions_from_grep_string(grep_string, project_id)
      extension_ids = [extension['id'] for extension in extensions]
      print('Disabling Extensions containing {}'.format(grep_string))
      await self.disable_extensions(extension_ids)
    else:
      await self.disable_extensions([extension_id])

  async def get_extensions_from_grep_string(self, grep_string, project_id):
    return getters.get_all_extensions_in_project(project_id, self.auth_options, getters.contains_grep_string,
                                                 grep_string=grep_string)

  async def disable_extensions(self, ids):
    tasks = []
    async with aiohttp.ClientSession() as session:
      for id in ids:
        task = asyncio.ensure_future(self.do_disable(id, session))
        tasks.append(task)
      responses = await asyncio.gather(*tasks)

      for extension_response in responses:
        extension_body = extension_response
        if extension_body.get('id'):
          print('Disabled Extension {}: {}'.format(extension_body['id'], extension_body['name']))
        else:
          print(extension_body)

  async def do_disable(self, extension_id, session):
    url = BASE_PATCH_URL.format(extension_id)
    async with session.patch(url, data=json.dumps({'enabled': False}), headers=self.auth_options) as response:
      return await response.json()

