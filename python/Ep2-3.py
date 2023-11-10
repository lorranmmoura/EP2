from neo4j import GraphDatabase

class Neo4jDriver:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None
        self._init_driver()

    def _init_driver(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def query_top_miyazaki_movies(self):
        with self._driver.session() as session:
            result = session.read_transaction(self._query_top_miyazaki_movies)
            return result

    @staticmethod
    def _query_top_miyazaki_movies(tx):
        query = (
            "MATCH (miyazaki:Person {name: 'Hayao Miyazaki'})-[:DIRECTED]->(movie:Movie) "
            "RETURN movie.title, movie.released "
            "ORDER BY movie.released ASC "
            "LIMIT 5"
        )
        return list(tx.run(query))

# Professor substitua essas informações com os detalhes do seu banco de dados local Neo4j
uri = "neo4j://localhost:7687"
user = "neo4j"
password = "imdb1234"

driver = Neo4jDriver(uri, user, password)
top_miyazaki_movies = driver.query_top_miyazaki_movies()

print("Top 5 filmes mais antigos de Hayao Miyazaki:")
for movie in top_miyazaki_movies:
    print(f"{movie['movie.title']} ({movie['movie.released']})")

driver.close()
