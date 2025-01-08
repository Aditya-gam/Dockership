# Dockership/config/db_config.py

import os  # OS module for accessing environment variables
# MongoClient for database operations, errors for exception handling
from pymongo import MongoClient, errors
# Type hinting for MongoDB collections
from pymongo.collection import Collection


class DBConfig:
    """
    MongoDB configuration class to manage connections, schema validation,
    and database operations for the Dockership application.
    """

    def __init__(self):
        """
        Initializes the DBConfig object with placeholders for the client and database connection.
        """
        self.client = None  # Placeholder for MongoDB client instance
        self.db = None  # Placeholder for MongoDB database instance

    def connect(self):
        """
        Establishes a connection to the MongoDB instance and ensures the database and critical collections exist.

        Returns:
            Database: A reference to the connected MongoDB database.

        Raises:
            RuntimeError: If the database connection or environment variable setup fails.
        """
        try:
            # Fetch the MongoDB URI from environment variables
            mongo_uri = os.getenv("MONGO_URI")
            if not mongo_uri:
                # Raise an error if the URI is not set
                raise ValueError(
                    "MONGO_URI is not set in the environment variables.")

            # Connect to MongoDB using the URI
            self.client = MongoClient(mongo_uri)

            # Connect to the specified database or default to "dockership"
            self.db = self.client[os.getenv("MONGO_DBNAME", "dockership")]

            # Ensure critical collections are initialized with proper schemas
            self._initialize_collections()

            return self.db  # Return the connected database instance

        # Handle database connection failure
        except errors.ConnectionFailure as e:
            raise RuntimeError(f"Database connection failed: {e}")

        # Handle missing or invalid environment variables
        except ValueError as e:
            raise RuntimeError(f"Environment error: {e}")

    def _initialize_collections(self):
        """
        Ensures required collections exist and validates their schemas (if applicable).

        This method is a simulation of schema enforcement, useful when working with MongoDB.
        """
        # Define schema requirements for each collection
        schemas = {
            "users": {
                "first_name": {"type": "string", "required": True, "max_length": 50},
                "last_name": {"type": "string", "required": False, "max_length": 50},
                "username": {"type": "string", "required": True, "unique": True, "max_length": 30},
            },
            "logs": {
                # Foreign key to users
                "username": {"type": "string", "required": True},
                # Log timestamp
                "timestamp": {"type": "datetime", "required": True},
                # Action performed
                "action": {"type": "string", "required": True},
                # Optional notes
                "notes": {"type": "string", "required": False},
            },
            "manifests": {
                # Foreign key to users
                "username": {"type": "string", "required": True},
                # Incoming manifest file
                "incoming_file": {"type": "string", "required": True},
                # Outgoing manifest file
                "outgoing_file": {"type": "string", "required": True},
            },
        }

        # Iterate through the defined schemas and ensure collections exist
        for collection, schema in schemas.items():
            self._ensure_collection_schema(collection, schema)

    def _ensure_collection_schema(self, collection_name, schema):
        """
        Ensures a collection exists and applies the schema (if schema validation is implemented).

        Args:
            collection_name (str): The name of the collection to initialize.
            schema (dict): The schema to apply (currently a placeholder for schema validation).
        """
        collection = self.db[collection_name]

        # Schema validation logic can be added here if using MongoDB validation rules (e.g., JSON Schema)
        # For now, this is a simulation.

    def get_collection(self, name) -> Collection:
        """
        Retrieves a specific collection from the connected database.

        Args:
            name (str): The name of the collection to retrieve.

        Returns:
            Collection: A reference to the requested MongoDB collection.

        Raises:
            RuntimeError: If the database connection is not initialized.
        """
        if self.db is None:  # Explicitly check if the database is uninitialized
            raise RuntimeError(
                "Database not initialized. Call connect() first.")
        return self.db[name]  # Return the requested collection

    def check_connection(self):
        """
        Checks if the connection to the MongoDB instance is successful.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            # Ping the MongoDB server to verify connectivity
            self.client.admin.command("ping")
            print("✅ MongoDB connection successful.")
            return True
        except Exception as e:
            # Print the error and return False if the connection check fails
            print(f"❌ MongoDB connection check failed: {e}")
            return False
