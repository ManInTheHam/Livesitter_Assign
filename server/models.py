from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
import json
from pathlib import Path
from bson.objectid import ObjectId

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/rtsp_overlay_app")
USE_FILE_DB = os.getenv("USE_FILE_DB", "false").lower() == "true"

# Simple file-based database for development
class FileDatabase:
    def __init__(self, db_file="overlays.json"):
        self.db_file = Path(__file__).parent / db_file
        self.data = self._load_data()
    
    def _load_data(self):
        if self.db_file.exists():
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_data(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def insert_one(self, data):
        # Generate a simple ID
        new_id = str(len(self.data) + 1)
        data_with_id = {"_id": new_id, **data}
        self.data.append(data_with_id)
        self._save_data()
        
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        
        return InsertResult(new_id)
    
    def find(self, query=None):
        if query is None:
            filtered_data = self.data
        else:
            # Simple query matching
            filtered_data = []
            for item in self.data:
                match = True
                for key, value in query.items():
                    if key not in item or item[key] != value:
                        match = False
                        break
                if match:
                    filtered_data.append(item)
        
        # Return a cursor-like object that supports sort
        class QueryResult:
            def __init__(self, data):
                self.data = data
            
            def sort(self, field, direction=-1):
                if field == "_id":
                    sorted_data = sorted(self.data, key=lambda x: int(x.get("_id", 0)), reverse=(direction == -1))
                else:
                    sorted_data = sorted(self.data, key=lambda x: x.get(field, ""), reverse=(direction == -1))
                return QueryResult(sorted_data)
            
            def __iter__(self):
                return iter(self.data)
        
        return QueryResult(filtered_data)
    
    def find_one(self, query):
        results = self.find(query)
        return results.data[0] if results.data else None
    
    def update_one(self, query, update):
        for i, item in enumerate(self.data):
            match = True
            for key, value in query.items():
                if key == "_id":
                    if item.get("_id") != value:
                        match = False
                        break
                elif key not in item or item[key] != value:
                    match = False
                    break
            
            if match:
                # Apply $set update
                if "$set" in update:
                    self.data[i].update(update["$set"])
                self._save_data()
                break
    
    def delete_one(self, query):
        for i, item in enumerate(self.data):
            match = True
            for key, value in query.items():
                if key == "_id":
                    if item.get("_id") != value:
                        match = False
                        break
                elif key not in item or item[key] != value:
                    match = False
                    break
            
            if match:
                del self.data[i]
                self._save_data()
                break
    


# Try MongoDB first, fall back to file database
if USE_FILE_DB:
    print("🗂️  Using file-based database for development")
    overlays = FileDatabase()
else:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command('ping')
        print(f"✅ Connected to MongoDB: {MONGO_URI}")
        
        db = client["rtsp_overlay_app"]
        overlays = db["overlays"]
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("🗂️  Falling back to file-based database for development")
        overlays = FileDatabase()
        
    except Exception as e:
        print(f"❌ MongoDB authentication error: {e}")
        print("🗂️  Falling back to file-based database for development")
        overlays = FileDa