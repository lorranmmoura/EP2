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

    def query_movies(self):
        with self._driver.session() as session:
            result = session.read_transaction(self._query_movies)
            return result

    @staticmethod
    def _query_movies(tx):
        query = (
            "MATCH (adamSandler:Person {name: 'Adam Sandler'})-[:ACTED_IN]->(movie:Movie) "
            "MATCH (robSchneider:Person {name: 'Rob Schneider'})-[:ACTED_IN]->(movie:Movie) "
            "WHERE NOT (movie)<-[:ACTED_IN]-(:Person {name: 'Drew Barrymore'}) "
            "RETURN movie.title"
        )
        return list(tx.run(query))

# Professor substitua essas informações com os detalhes do seu banco de dados local Neo4j
uri = "neo4j://localhost:7687" 
user = "neo4j"  
password = "imdb1234"  

driver = Neo4jDriver(uri, user, password)
movies = driver.query_movies()

print("Filmes onde Adam Sandler e Rob Schneider aparecem juntos, mas não atuam com Drew Barrymore:")
for movie in movies:
    print(movie["movie.title"])

driver.close()

