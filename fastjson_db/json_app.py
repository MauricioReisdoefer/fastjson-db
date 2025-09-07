import orjson

class JsonApp():
    """Base engine for the FastJson-DB framework"""
    def __init__(self):
        """Starts the application"""
        self._TABLE_REGISTRY = {} # Stores all JsonTables with key-value (JsonModel, JsonTable)
        self._loadTables()
        self._loadCache()
        pass
    
    def _loadCache(self):
        """Loads the .json tables in cache"""
        pass
    
    def _loadTables(self):
        """Loads every .json table in _TABLE_REGISTRY in intialization"""
        pass
    
    def _flushDatabase(self):
        """Load .log operations in the .json tables"""
        pass
    
    def _discoverTables(self):
        """Discover created .json files and assert they are registred in _TABLE_REGISTRY"""
    
    def registerTable(self):
        """Add a new tabble to the _tables list and _tables registry"""
        pass