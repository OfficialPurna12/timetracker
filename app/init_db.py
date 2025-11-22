from app import create_app, mongo
from bson import ObjectId
from datetime import datetime

def init_database():
    app = create_app()
    
    with app.app_context():
        try:
            # Get database instance
            db = mongo.db
            
            print("Connected to database:", db.name)
            
            # List of required collections
            collections = ['users', 'subjects', 'study_sessions', 'goals']
            
            print("\nChecking collections...")
            existing_collections = db.list_collection_names()
            print("Existing collections:", existing_collections)
            
            # Create collections if they don't exist
            for collection_name in collections:
                if collection_name not in existing_collections:
                    print(f"Creating collection: {collection_name}")
                    db.create_collection(collection_name)
                else:
                    print(f"Collection {collection_name} already exists")
            
            print("\nCreating indexes...")
            
            # Create indexes for better performance
            try:
                db.users.create_index('email', unique=True)
                print("✓ Created unique index on users.email")
            except Exception as e:
                print(f"✓ Index on users.email already exists: {e}")
            
            try:
                db.subjects.create_index('user_id')
                print("✓ Created index on subjects.user_id")
            except Exception as e:
                print(f"✓ Index on subjects.user_id already exists: {e}")
            
            try:
                db.study_sessions.create_index('user_id')
                print("✓ Created index on study_sessions.user_id")
            except Exception as e:
                print(f"✓ Index on study_sessions.user_id already exists: {e}")
            
            try:
                db.study_sessions.create_index('session_date')
                print("✓ Created index on study_sessions.session_date")
            except Exception as e:
                print(f"✓ Index on study_sessions.session_date already exists: {e}")
            
            try:
                db.study_sessions.create_index([('user_id', 1), ('start_time', -1)])
                print("✓ Created compound index on study_sessions")
            except Exception as e:
                print(f"✓ Compound index on study_sessions already exists: {e}")
            
            try:
                db.goals.create_index('user_id')
                print("✓ Created index on goals.user_id")
            except Exception as e:
                print(f"✓ Index on goals.user_id already exists: {e}")
            
            # Insert sample data for testing (optional)
            print("\nChecking for sample data...")
            
            # Check if we have any users
            user_count = db.users.count_documents({})
            if user_count == 0:
                print("No users found. You can register a new user through the web interface.")
            else:
                print(f"Found {user_count} user(s) in the database")
            
            # Count documents in each collection
            print("\nDocument counts:")
            for collection_name in collections:
                count = db[collection_name].count_documents({})
                print(f"  {collection_name}: {count} documents")
            
            print("\n" + "="*50)
            print("✅ Database initialization completed successfully!")
            print("="*50)
            
        except Exception as e:
            print(f"❌ Error during database initialization: {e}")
            print("Please check your MongoDB connection and try again.")

def check_database_connection():
    """Simple function to test database connection"""
    app = create_app()
    
    with app.app_context():
        try:
            # Test the connection
            db = mongo.db
            # This will raise an exception if not connected
            db.command('ping')
            print("✅ MongoDB connection successful!")
            return True
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            return False

if __name__ == '__main__':
    print("Starting StudyMate Database Initialization...")
    print("="*50)
    
    # First check connection
    if check_database_connection():
        # Then initialize database
        init_database()
    else:
        print("\n❌ Cannot initialize database. Please check:")
        print("1. Is MongoDB running?")
        print("2. Is the MONGODB_URI correct in config.py?")
        print("3. For local MongoDB: run 'mongod' in terminal")
        print("4. For MongoDB Atlas: check your connection string")