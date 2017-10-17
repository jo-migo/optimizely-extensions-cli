from bravado.client import SwaggerClient
from bravado_asyncio.http_client import AsyncioClient

OPTIMIZELY_BASE_URL = 'https://api.optimizely.com/v2/'
def load_swagger_client():
  client = SwaggerClient.from_url('https://api.optimizely.com/swagger.json',
                                  config={'also_return_response': True},
                                  http_client=AsyncioClient())
  client.swagger_spec.api_url = OPTIMIZELY_BASE_URL
  return client
