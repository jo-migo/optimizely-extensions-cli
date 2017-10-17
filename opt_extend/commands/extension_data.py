"""Accumulate data about a certain Extension"""
import texttable

from .base import *

from .common import authorization

class ExtensionData(Base):
  """
  Gather usage data about a given Extension

  Usage:

  opt-extend extension_data <extension_id> <project_id> [--page_id=<page_id>] [--json]
  """

  async def run(self):
    extension_id = self.options.get('<extension_id>')
    project_id = self.options.get('<project_id>')
    as_json = self.options.get('--json')
    self.auth_options = authorization.get_token_for_project(project_id)

    page_id = self.options.get('--page_id', None)
    experiment_data = self.get_experiment_data(extension_id, page_id)
    if experiment_data:
      if as_json:
        print(experiment_data)
      else:
        format_and_print_experiment_data(experiment_data)
    else:
      print('No usage data found for extension {}'.format(extension_id))

  def get_experiment_data(self, extension_id, page_id=None):
    experiment_data = []

    extension, _ = self.client.Extensions.get_extension(extension_id=extension_id,
                                                        _request_options={"headers": self.auth_options}).result()
    initial_statement = 'Generating Extension Usage Data for Extension {}'.format(extension['name'])
    if page_id:
      initial_statement += '-- On Page {}'.format(page_id)
    print(initial_statement)
    i = 1
    project_id = extension['project_id']

    while True:
      exp_request = self.client.Experiments.list_experiments(project_id=project_id, page=i, per_page=100,
                                                        _request_options={"headers": self.auth_options})
      experiments, http_resp = exp_request.result()
      for x in experiments:
        variations = x['variations']
        for v in variations:
          if v.actions:
            for action in v.actions:
              for change in action.changes:
                if change.extension_id:
                  if change.extension_id == extension_id:
                    if not page_id or int(page_id) == action.page_id:
                      experiment_data.append({
                        'experiment_name': x.name,
                        'experiment_id': str(x.id),
                        'variation_name': v.name,
                        'variation_id': str(v.variation_id),
                        'extension_config': change.config,
                        'variation_status': compute_variation_status(v.archived, x.status),
                        'page_id': action.page_id
                      }
                    )
      if 'next' not in (http_resp.headers.get('Link') or []):
        return experiment_data
      i += 1


def compute_variation_status(variation_archived, experiment_status):
  """ Computes the status of the variation containing the extension """
  if variation_archived is True or experiment_status == 'archived':
    return 'Archived'
  elif variation_archived is False and experiment_status in ['paused', 'campaign_paused']:
    return 'Experiment Paused'
  elif variation_archived is False and experiment_status == 'not_started':
    return 'Not Started'
  else:
    return 'Running'


def format_and_print_experiment_data(variation_data):
  "Prints the data for all variations an Extension is involved in "

  extensions_table = texttable.Texttable()
  extensions_table.set_deco(texttable.Texttable.HEADER)
  extensions_table.set_cols_width([25, 15, 25, 15, 20, 15])
  extensions_table.set_cols_dtype(['t',
                                   'i',
                                   't',
                                   'i',
                                   't',
                                   'i'])
  extensions_table.set_cols_align(["l", "l", "l", "l", "l", "l"])
  table_contents = [
    ['Experiment Name', 'Experiment ID', 'Variation Name', 'Variation ID', 'Variation Status', 'Page ID']]

  for variation in variation_data:
    row_data = [variation.get('experiment_name'), variation.get('experiment_id'), variation.get('variation_name'),
                variation.get('variation_id'), variation.get('variation_status'), variation.get('page_id')]
    table_contents.append(row_data)
  extensions_table.add_rows(table_contents)
  print(extensions_table.draw())
