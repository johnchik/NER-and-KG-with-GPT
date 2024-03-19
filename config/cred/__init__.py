from src.shared.utils import Credential_OpenAI
from src.shared.utils import Credential_Azure
class Infra:
    AZURE_OPENAI_CREDENTIAL: Credential_Azure = dict(
        azure_endpoint='https://cuhk-api-dev1-apim1.azure-api.net',
        api_version = '2023-05-15',
        api_key = "xxx" # please input your own azure api_key
    )
    
    # If you want to use openai other than Azure
    OPENAI_CREDENTIAL: Credential_OpenAI = dict(
        api_key = "sk-xxx", # please input your own openai api_key
    )
    NEO4J_CREDENTIAL = dict(
        uri = "bolt://localhost:7687",
        auth = ("neo4j", "xxx")
    )
    