from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)

class Database:
    """MongoDB database handler"""
    
    client = None
    db = None
    
    @staticmethod
    def init_db(app):
        """Initialize database connection"""
        try:
            Database.client = MongoClient(
                app.config['MONGO_URI'],
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            Database.client.admin.command('ping')
            
            Database.db = Database.client[app.config['DATABASE_NAME']]
            
            logger.info(f"Connected to MongoDB database: {app.config['DATABASE_NAME']}")
            
            # Create indexes for better performance
            Database._create_indexes(app)
            
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Database initialization error: {str(e)}")
            raise
    
    @staticmethod
    def _create_indexes(app):
        """Create database indexes"""
        try:
            collection = Database.db[app.config['COLLECTION_NAME']]
            
            # Create indexes
            collection.create_index('created_at')
            collection.create_index('priority')
            collection.create_index('completed')
            collection.create_index('due_date')
            
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.warning(f"Failed to create indexes: {str(e)}")
    
    @staticmethod
    def get_collection(collection_name):
        """Get a collection from the database"""
        if Database.db is None:
            raise Exception("Database not initialized")
        return Database.db[collection_name]
    
    @staticmethod
    def close_connection():
        """Close database connection"""
        if Database.client:
            Database.client.close()
            logger.info("Database connection closed")

def init_db(app):
    """Initialize database (wrapper function)"""
    Database.init_db(app)

def get_db():
    """Get database instance"""
    return Database.db