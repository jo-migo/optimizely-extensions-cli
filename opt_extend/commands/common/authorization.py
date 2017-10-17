import configparser
import os

AUTH_PROMPT = 'Please enter your Optimizely API token for this project: '
AUTH_DIRECTORY = '/Users/jgoergen/optimizely_auth/token.txt'
AUTH_CONFIG = '{}/{}.cfg'.format(os.path.expanduser('~'), '.optimizely-config')


def get_token_for_project(project_id):
  configured_token = get_token_for_project__from_config(project_id)
  if configured_token:
    token = configured_token
  else:
    token = str(input(AUTH_PROMPT))
  return {'Authorization': "Bearer {}".format(token)}


def get_token_for_project__from_config(project_id):
  config = configparser.RawConfigParser()
  if os.path.exists(AUTH_CONFIG):
    config.read(AUTH_CONFIG)
    if config.has_section(str(project_id)):
      return config.get(str(project_id), 'token')

def remove_token_for_project__from_config(project_id):
  config = configparser.RawConfigParser()
  if os.path.exists(AUTH_CONFIG):
    config.read(AUTH_CONFIG)
    if config.has_section(str(project_id)):
      return config.remove_section(str(project_id))
  return False
