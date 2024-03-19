from typing import TypedDict
from opencc import OpenCC

class Credential_Azure(TypedDict):
    deployment_id: str
    api_version: str
    api_key: str


class Credential_OpenAI(TypedDict):
    api_key: str
    base_url: str


def passage_splitter(passage: str, length: int = 1000) -> tuple[str, str]:
    if len(passage) > length:
        input = passage[:length]
        return input, passage[length:]
    return passage, ""

def fix_characters(s):
    s = s.replace('《', '')
    s = s.replace('》', '')
    s = s.replace('．', '')
    s = s.replace('·', '')
    s = s.replace('＋','十')
    s = s.replace('、', '')
    s = s.replace('「','')
    s = s.replace('」','')
    s = s.replace('︺','')

    return s

def convert_string_to_block(nodes, relationships):
    query = ""
    for node in nodes:
        query += node
        query += '\n'

    for relationship in relationships:
        query += relationship
        query += '\n'

    query = fix_characters(query)
    cc = OpenCC('s2t')
    return cc.convert(query)
