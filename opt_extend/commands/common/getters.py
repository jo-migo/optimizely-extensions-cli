import re

from .swagger_client import *


def get_all_extensions_in_project(project_id, auth, filter_callback=None, **filter_callback_kwargs):
    client = load_swagger_client()
    i = 1
    all_extensions = []
    while True:
        request = client.Extensions.list_extensions(project_id=project_id, page=i,
                                                    _request_options={"headers": auth})
        extensions, http_resp = request.result()
        if filter_callback:
            all_extensions += filter_callback(extensions, **filter_callback_kwargs)
        else:
            all_extensions += extensions
        if 'next' not in (http_resp.headers.get('Link') or []):
            break
        i += 1

    return all_extensions

def contains_grep_string(extensions_json, grep_string=''):
  filtered = []
  for extension in extensions_json:
    extension_string = str(extension)
    if re.search(grep_string, extension_string):
      filtered.append(extension)
  return filtered
