from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime, date, timedelta
import bcrypt

class User:
    @staticmethod
    def create_user(mongo, email, password, name):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {
            'email': email,
            'password_hash': hashed_password,
            'name': name,
            'daily_goal_hours': 2,
            'preferred_timer_duration': 25,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return mongo.db.users.insert_one(user)
    
    @staticmethod
    def find_by_email(mongo, email):
        return mongo.db.users.find_one({'email': email})
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

class Subject:
    @staticmethod
    def create_subject(mongo, user_id, name, color, icon, weekly_goal_hours):
        subject = {
            'user_id': ObjectId(user_id),
            'name': name,
            'color': color,
            'icon': icon,
            'weekly_goal_hours': weekly_goal_hours,
            'created_at': datetime.utcnow()
        }
        return mongo.db.subjects.insert_one(subject)
    
    @staticmethod
    def get_user_subjects(mongo, user_id):
        return list(mongo.db.subjects.find({'user_id': ObjectId(user_id)}))
    
    @staticmethod
    def delete_subject(mongo, subject_id, user_id):
        return mongo.db.subjects.delete_one({'_id': ObjectId(subject_id), 'user_id': ObjectId(user_id)})

class StudySession:
    @staticmethod
    def create_session(mongo, user_id, subject_id, duration_minutes):
        # Convert date to datetime for MongoDB compatibility
        session_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        session = {
            'user_id': ObjectId(user_id),
            'subject_id': ObjectId(subject_id),
            'start_time': datetime.utcnow(),
            'duration_minutes': duration_minutes,
            'session_date': session_date,  # Use datetime instead of date
            'created_at': datetime.utcnow()
        }
        return mongo.db.study_sessions.insert_one(session)
    
    @staticmethod
    def get_today_sessions(mongo, user_id):
        # Use datetime for today's date
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        return list(mongo.db.study_sessions.find({
            'user_id': ObjectId(user_id),
            'session_date': today
        }))
    
    @staticmethod
    def get_weekly_sessions(mongo, user_id):
        week_ago = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
        return list(mongo.db.study_sessions.find({
            'user_id': ObjectId(user_id),
            'start_time': {'$gte': week_ago}
        }))

class Goal:
    @staticmethod
    def create_goal(mongo, user_id, title, description, target_date):
        # Convert date to datetime for MongoDB
        if isinstance(target_date, date):
            target_date = datetime.combine(target_date, datetime.min.time())
            
        goal = {
            'user_id': ObjectId(user_id),
            'title': title,
            'description': description,
            'target_date': target_date,
            'is_completed': False,
            'created_at': datetime.utcnow()
        }
        return mongo.db.goals.insert_one(goal)
    
    @staticmethod
    def get_user_goals(mongo, user_id):
        return list(mongo.db.goals.find({'user_id': ObjectId(user_id)}))