from openai import OpenAI
from src.infrastructure.azure_cuhk import AzureOpenAI_CUHK
from src.shared.utils import passage_splitter
import json

class NamedEntityRecognition_RelationshipExtraction():
    prompt = """Please perform named entity recognition on the following news article text and identify the relationships between the entities. Specifically, I'm interested in relationships involving Person, Organization, Location and Event that are relevant to the context of the news article. Output the entities as new nodes created in neo4j using Cypher. For each relationship, please describe the nature of the relationship using the Cypher query language as well using verbs or verb phrases in english. For example,

Example text:

政府推動的大型盛事之一、香港設計中心策展的「Chubby Hearts Hong Kong」在2月14日情人節啟動。由著名設計師Anya Hindmarch構思的直徑12米巨型紅色Chubby Hearts，率先於中環皇后像廣場花園飄浮，而直徑3米的Chubby Hearts也於另外三個地方「快閃」展示。

活動會一直舉行至2月24日正月十五「中國情人節」元宵節。期間「大心」、直徑12米的Chubby Hearts會長駐中環皇后像廣場花園，而「細心」、直徑3米的Chubby Hearts則會每日在不同地方「快閃」飄浮，供市民打卡。

The format of the answer is (and only contains):
Output:{
    \"nodes\":[
        \"CREATE (anya:Person {name: \'Anya Hindmarch\', role: \'著名設計師\'})\", 
        \"CREATE (chubby:Event {name: \'Chubby Hearts Hong Kong\'})\", 
        \"CREATE (香港政府:Organization {name: \'香港政府\'})\", 
        \"CREATE (香港設計中心:Organization {name: \'香港設計中心\'})\", 
        \"CREATE (皇后像廣場花園:Location {name:\'皇后像廣場花園\'})\", 
        \"CREATE (中環:Location {name:\'中環\'})\"
    ],
    \"relationships\": [
        \"CREATE (chubby)-[:LOCATED_IN]->(皇后像廣場花園)\", 
        \"CREATE (皇后像廣場花園)-[:LOCATED_IN]->(中環)\", 
        \"CREATE (香港政府)-[:PROMOTED]->(chubby)\", 
        \"CREATE (anya)-[:DESIGNED]->(chubby)\", 
        \"CREATE (香港設計中心)-[:ORGANIZED]->(chubby)\"
    ]
}

End of example.

Now, perform the same for the following news article. Try to be aggresive and it is always better to include all proper nouns as entities.

"""

    def __init__(self, client: OpenAI) -> None:
        self.client = client
        if isinstance(self.client, AzureOpenAI_CUHK):
            self.model_name = "gpt-35-turbo"
        else:
            self.model_name = "gpt-3.5-turbo"


    def build_prompt(self, text) -> str:
        return f"Text 2: {text}\nOutput: "


    def execute(self, passage: str) -> dict:
        output_nodes = []
        output_relationships = []
        pending_raw_outputs = []

        while passage != '':
            input, passage = passage_splitter(passage, length=2000)
            query = self.build_prompt(input)
            
            completion = self.client.chat.completions.create(
                model=self.model_name,
                temperature=0,
                messages=[{"role": "user", "content": self.prompt+query}],
                stream=False,
                frequency_penalty=0.5
            )
            try:
                temp_output = json.loads(completion.choices[0].message.content.strip('Output:'))
            
                if 'nodes' in temp_output.keys():
                    output_nodes.append(temp_output['nodes'])

                if 'relationships' in temp_output.keys():
                    output_relationships.append(temp_output['relationships'])
            
            except json.decoder.JSONDecodeError:
                pending_raw_outputs.append(completion.choices[0].message.content.strip('Output:'))

        if pending_raw_outputs != []:
            return {"nodes": output_nodes, "relationships": output_relationships, 'raw_outputs': pending_raw_outputs}
        else:
            return {"nodes": output_nodes, "relationships": output_relationships}
