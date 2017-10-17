"""The base command."""
from .common import swagger_client

class Base(object):
  """A base command."""

  def __init__(self, options, *args, **kwargs):
    self.options = options
    self.args = args
    self.kwargs = kwargs
    self.client = swagger_client.load_swagger_client()
    self.authorization = None

  async def run(self):
    raise NotImplementedError('You must implement the run() method yourself!')
