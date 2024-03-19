from src.infrastructure.azure_cuhk import AzureOpenAI_CUHK
from openai import OpenAI
from neo4j import GraphDatabase

from config.cred import Infra

class Engine:
    client = AzureOpenAI_CUHK(**Infra.AZURE_OPENAI_CREDENTIAL)
    # client = OpenAI(**Infra.OPENAI_CREDENTIAL)
    neo4j_db = GraphDatabase.driver(**Infra.NEO4J_CREDENTIAL)
