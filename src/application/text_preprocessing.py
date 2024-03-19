from openai import OpenAI
from src.infrastructure.azure_cuhk import AzureOpenAI_CUHK
from src.shared.utils import passage_splitter

class TextPreprocessing():
    def __init__(self, client: OpenAI) -> None:
        self.client = client
        if isinstance(self.client, AzureOpenAI_CUHK):
            self.model_name = "gpt-35-turbo"
        else:
            self.model_name = "gpt-3.5-turbo"


    def execute(self, passage: str) -> str:
        output_list = []
        while passage != '':
            input, passage = passage_splitter(passage)
            query = f'目標：根據前文後理和中文詞義，把下列香港文章中經OCR提取的錯誤漢字或詞語改正為繁體中文\n\n文章：{input}\n輸出：'

            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": query}],
                stream=False, 
                temperature=0
            )
            
            corrected_text = completion.choices[0].message.content
            output_list.append(corrected_text)
        output = "".join(output_list)
        return output
