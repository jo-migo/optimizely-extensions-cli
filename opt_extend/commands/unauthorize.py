import os

from .common import authorization
from .base import *

class Unauthorize(Base):
  """
  Either delete a specific token from Optimizely config or delete entire config

  Usage:
    opt-extend unauthorize ( --project-id=<project_id> | --all )
  """
  async def run(self):
    project_id = self.options.get('--project-id')
    delete_all = self.options.get('--all')
    if delete_all:
        try:
            os.remove(authorization.AUTH_CONFIG)
            print('Removed all authorization tokens from configuration.')
        except OSError:
            print('No authorization configuration found.')
    else:
        if authorization.remove_token_for_project__from_config(project_id):
            print('Removed authorization for project {}.'.format(project_id))
        else:
            print('No authorization configuration found for project {}.'.format(project_id))
