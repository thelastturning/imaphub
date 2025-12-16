from arango import ArangoClient as PyArangoClient
from arango.database import StandardDatabase
import os

class ArangoClient:
    """
    Wrapper for ArangoDB connection management.
    """
    def __init__(self):
        self._client = PyArangoClient(hosts=os.getenv("ARANGO_HOST", "http://db:8529"))
        self._sys_db = self._client.db(
            "_system",
            username=os.getenv("ARANGO_USER", "root"),
            password=os.getenv("ARANGO_PASSWORD", "")
        )
        self._db_name = os.getenv("ARANGO_DB", "imap_hub")
        
        # Ensure database exists
        if not self._sys_db.has_database(self._db_name):
            self._sys_db.create_database(self._db_name)
            
        self.db: StandardDatabase = self._client.db(
            self._db_name,
            username=os.getenv("ARANGO_USER", "root"),
            password=os.getenv("ARANGO_PASSWORD", "")
        )

    def get_db(self) -> StandardDatabase:
        return self.db

async def get_arango_db() -> StandardDatabase:
    """
    Dependency injection provider.
    """
    client = ArangoClient()
    return client.get_db()
