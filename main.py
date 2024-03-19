"""
In the file, we will demonstrate the workflow of 
1. Text Preprecess
2. NER and Relationship Extraction
"""

from config import Engine
from src.application.text_preprocessing import TextPreprocessing
from src.application.ner_with_relationship import NamedEntityRecognition_RelationshipExtraction
from src.domain.parsed_text import ParsedText
from sample import *
import json

def main():
    text_preprocessor = TextPreprocessing(Engine.client)
    source = TEXT_SOURCE # If you use your own api key, then you can change any passage you want
    try:
        output = text_preprocessor.execute(source)
        parsed = ParsedText(source=TEXT_SOURCE, output=output)
        print(output)
    except:
        print("It seems you did not provide your own api key")
        print("The example will use pre-defined output instead.")
        output = TEXT_OUTPUT
        parsed = ParsedText(source=TEXT_SOURCE, output=output)
        print(output)

    print(f"Modified Word Count = {parsed.modified_word_count()}")
    print(f"Estimated Price (USD) = {parsed.token_price_usage_estimation()['total_price']:.3f}")

    ner = NamedEntityRecognition_RelationshipExtraction(Engine.client)
    try:
        result = ner.execute(output)
        print(json.dumps(result, indent=4, ensure_ascii=False))
    except:
        print("It seems you did not provide your own api key")
        print("The example will use pre-defined output instead.")
        print(json.dumps(NER_OUTPUT, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()