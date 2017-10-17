import os

def expand_options(options):
  if not options:
    return {}

  options_json = {'choices': []}
  if options.choices is not None:
    for choice in options.choices:
      options_json['choices'].append(choice)
  return options_json

def generate_file_path(directory_name, file_name):
  directory_path = os.path.expanduser(directory_name)
  return directory_path.rstrip('/') + '/' + file_name
