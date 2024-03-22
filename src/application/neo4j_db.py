from neo4j._sync.driver import Driver
from src.shared.utils import convert_string_to_block


class Neo4jDB():
    def __init__(self, client_db: Driver) -> None:
        self.client_db = client_db


    def execute(self, nodes: list[str], relationships: list[str]):
        self.client_db.verify_connectivity()

        summary = self.client_db.execute_query(
            convert_string_to_block(nodes, relationships),
            database_="neo4j"
        ).summary

        nodes_created = summary.counters.nodes_created
        relationships_created = summary.counters.relationships_created
        
        print(f"{nodes_created = }, {relationships_created = }")

        # This deletes nodes without names
        self.client_db.execute_query(
            "MATCH (n) WHERE size(labels(n)) = 0 DETACH DELETE n",
            database_="neo4j"
        )

        # These four commands merge similar nodes
        # Note : Neo4j database must have the apoc package installed to run the following
        self.client_db.execute_query(
            "MATCH (n:Organization) WITH toLower(n.name) as name, collect(n) as nodes CALL apoc.refactor.mergeNodes(nodes) yield node RETURN *",
            database_="neo4j"
        )

        self.client_db.execute_query(
            "MATCH (n:Person) WITH toLower(n.name) as name, collect(n) as nodes CALL apoc.refactor.mergeNodes(nodes) yield node RETURN *",
            database_="neo4j"
        )

        self.client_db.execute_query(
            "MATCH (n:Location) WITH toLower(n.name) as name, collect(n) as nodes CALL apoc.refactor.mergeNodes(nodes) yield node RETURN *",
            database_="neo4j"
        )

        self.client_db.execute_query(
            "MATCH (n:Event) WITH toLower(n.name) as name, collect(n) as nodes CALL apoc.refactor.mergeNodes(nodes) yield node RETURN *",
            database_="neo4j"
        )
    