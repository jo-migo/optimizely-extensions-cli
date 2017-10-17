"""The list command."""
import texttable

from .common import authorization
from .common import getters
from .base import *

CLIENT = None
AUTH_OPTIONS = {}


class List(Base):
  """List the Extensions in the current project"""

  async def run(self):

    project_id = self.options.get('<project_id>')
    export_json = self.options.get('--json')
    self.auth_options = authorization.get_token_for_project(project_id)
    self.display_extensions_in_project(project_id, export_json)

  def display_extensions_in_project(self, project_id, as_json=False):
    all_extensions = getters.get_all_extensions_in_project(project_id, self.auth_options)
    if as_json:
      print(all_extensions)
    else:
      print_extensions_table(all_extensions)


def print_extensions_table(extensions):
  extensions_table = texttable.Texttable()
  extensions_table.set_deco(texttable.Texttable.HEADER)
  extensions_table.set_cols_width([40, 15, 15])
  extensions_table.set_cols_dtype(['t', 'i', 't'])
  extensions_table.set_cols_align(["l", "l", "l"])
  table_contents = [['Extension Name', 'Extension ID', 'Enabled']]

  for extension in extensions:
    row_data = [extension.name, extension.id, extension.enabled]
    table_contents.append(row_data)
  extensions_table.add_rows(table_contents)
  print(extensions_table.draw())
