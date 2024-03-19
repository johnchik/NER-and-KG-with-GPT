from difflib import SequenceMatcher
import tiktoken

class ParsedText:
    
    
    def __init__(self, source: str, output: str) -> None:
        assert type(source) == type(output) == str, "The input parameter must be str!"
        self.source = source
        self.output = output
    
    
    def modified_word_count(self) -> int:
        app=SequenceMatcher(None, self.source, self.output)
        matching_blks=app.get_matching_blocks()

        modified_count=sum([len(range(matching_blks[i].a+matching_blks[i].size, matching_blks[i+1].a)) for i in range(0, len(matching_blks)-1)])
        
        return modified_count
    

    def token_price_usage_estimation(self) -> int:
        # Please note that the estimation will be inaccurate 
        # if you have modified the output.

        encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
        source_token = len(encoder.encode_batch(self.source))
        output_token = len(encoder.encode_batch(self.output))
        total_token = source_token + output_token

        input_pricing = 0.0015/1000
        output_pricing = 0.002/1000
        total_price = source_token*input_pricing + output_token*output_pricing
        return dict(
            total_token=total_token,
            total_price=total_price
        )