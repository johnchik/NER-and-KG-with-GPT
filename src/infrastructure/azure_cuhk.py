from openai import AzureOpenAI
from openai._models import FinalRequestOptions
from openai._base_client import SyncAPIClient
from openai._version import __version__

class AzureOpenAI_CUHK(AzureOpenAI):
    def _prepare_options(self, options: FinalRequestOptions) -> None:
        headers: dict = {}
        options.headers = headers
        headers['Ocp-Apim-Subscription-Key'] = self.api_key
        
        return SyncAPIClient(
            version=__version__, 
            base_url=self.base_url,
            _strict_response_validation=False
        )._prepare_options(options)
