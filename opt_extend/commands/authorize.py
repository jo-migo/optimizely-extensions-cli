import configparser
import sys

from .common import authorization
from .base import *

class Authorize(Base):
  """Authorize with Optimizely

  WARNING: This initializes a file in $HOME that can be removed with the RemoveAuth command
  When executing commands, the CLI looks for Personal Access Tokens in the following order:
  - Uses --authorization=<personal_access_token> option if provided
  - Looks for authorization in $HOME/.opt-extend-profiles
    - If a --profile=<profile_name> option is provided, looks for the specified profile
    - Else, uses 'default'
  - Asks for authorization with a prompt if neither of above are satisfied

  Usage:
  opt-extend authorize <project_id> <token>

  [default]
  auth-mode=password
  username=bsmith
  password=abc123

  [system1]
  auth-mode=oauth
  auth-token=abc-123
  auth-url=http://system.1/authenticate

  [system2]
  auth-mode=anonymous
  auth-url=http://this-is.system2/start
  """

  async def run(self):
    project_id = self.options.get('<project_id>')
    auth_token = self.options.get('<token>')
    create_or_update_config(project_id, auth_token)


def create_or_update_config(project_id, auth_token):
  config = configparser.RawConfigParser()
  if authorization.get_token_for_project__from_config(project_id) is not None:
    replace_token = input('Authorization token for project {} already found. Proceed anyway?'.format(project_id))
    if not replace_token:
      print('Skipping re-authorization')
      sys.exit()
    config.remove_section(str(project_id))
  config.add_section(str(project_id))
  config.set(str(project_id), 'token', auth_token)
  # Writing to file to '$HOME/.optimizely-config.cfg'
  with open(authorization.AUTH_CONFIG, 'w') as configfile:
    config.write(configfile)
  print ('Added authorization for project {}'.format(project_id))
