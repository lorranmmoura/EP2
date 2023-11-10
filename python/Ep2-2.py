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

    def query_shared_year_movies(self):
        with self._driver.session() as session:
            result = session.read_transaction(self._query_shared_year_movies)
            return result

    @staticmethod
    def _query_shared_year_movies(tx):
        query = (
            "MATCH (sandler:Person {name: 'Adam Sandler'})-[:ACTED_IN]->(sandlerMovie:Movie) "
            "MATCH (miyazaki:Person {name: 'Hayao Miyazaki'})-[:DIRECTED]->(miyazakiMovie:Movie) "
            "WHERE sandlerMovie.released = miyazakiMovie.released "
            "RETURN sandlerMovie.title AS sandlerTitle, sandlerMovie.released AS sharedYear, "
            "miyazakiMovie.title AS miyazakiTitle "
            "ORDER BY sharedYear ASC"
        )
        return list(tx.run(query))

# Professor substitua essas informações com os detalhes do seu banco de dados local Neo4j
uri = "neo4j://localhost:7687"
user = "neo4j"
password = "imdb1234"

driver = Neo4jDriver(uri, user, password)
shared_year_movies = driver.query_shared_year_movies()

print("Filmes de Adam Sandler e Hayao Miyazaki lançados no mesmo ano:")
print("Adam Sandler\t\tHayao Miyazaki\t\tAno Comum")
print("="*70)

for movie_pair in shared_year_movies:
    print(f"{movie_pair['sandlerTitle']}\t\t{movie_pair['miyazakiTitle']}\t\t{movie_pair['sharedYear']}")

driver.close()
