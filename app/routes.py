from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from bson import ObjectId
from datetime import datetime, date, timedelta
from app.forms import SubjectForm, GoalForm
from app.models import Subject, StudySession, Goal
from app import mongo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'user_id' not in session:
        return render_template('index.html')
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    # Get user's subjects
    subjects = Subject.get_user_subjects(mongo.db, user_id)
    
    # Get today's sessions
    today_sessions = StudySession.get_today_sessions(mongo.db, user_id)
    total_today_minutes = sum(session['duration_minutes'] for session in today_sessions)
    
    # Get weekly progress
    weekly_sessions = StudySession.get_weekly_sessions(mongo.db, user_id)
    
    # Calculate subject-wise progress
    subject_progress = {}
    for subject in subjects:
        subject_sessions = [s for s in today_sessions if str(s['subject_id']) == str(subject['_id'])]
        subject_today_minutes = sum(s['duration_minutes'] for s in subject_sessions)
        subject_progress[str(subject['_id'])] = {
            'today_minutes': subject_today_minutes,
            'daily_goal_minutes': subject.get('weekly_goal_hours', 1) * 60 / 7
        }
    
    return render_template('dashboard.html', 
                         subjects=subjects,
                         total_today_minutes=total_today_minutes,
                         subject_progress=subject_progress,
                         weekly_sessions=weekly_sessions,
                         now=datetime.utcnow())

@main.route('/timer')
def timer():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    subjects = Subject.get_user_subjects(mongo.db, session['user_id'])
    return render_template('timer.html', subjects=subjects)

@main.route('/progress')
def progress():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    subjects = Subject.get_user_subjects(mongo.db, user_id)
    weekly_sessions = StudySession.get_weekly_sessions(mongo.db, user_id)
    
    # Calculate streak
    streak = calculate_streak(mongo.db, user_id)
    
    # Prepare chart data
    chart_data = prepare_chart_data(subjects, weekly_sessions)
    
    return render_template('progress.html', 
                         subjects=subjects,
                         weekly_sessions=weekly_sessions,
                         streak=streak,
                         chart_data=chart_data,
                         now=datetime.utcnow())

@main.route('/subjects', methods=['GET', 'POST'])
def subjects():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    form = SubjectForm()
    if form.validate_on_submit():
        Subject.create_subject(mongo.db, 
                             session['user_id'],
                             form.name.data,
                             form.color.data,
                             form.icon.data,
                             form.weekly_goal_hours.data)
        flash('Subject added successfully!', 'success')
        return redirect(url_for('main.subjects'))
    
    user_subjects = Subject.get_user_subjects(mongo.db, session['user_id'])
    return render_template('subjects.html', form=form, subjects=user_subjects)

@main.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('settings.html', now=datetime.utcnow())

# API Routes
@main.route('/api/start_timer', methods=['POST'])
def start_timer():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    subject_id = data.get('subject_id')
    duration = data.get('duration')
    
    if not subject_id or not duration:
        return jsonify({'error': 'Missing parameters'}), 400
    
    # In a real app, you might want to track active timers
    return jsonify({'success': True, 'message': 'Timer started'})

@main.route('/api/stop_timer', methods=['POST'])
def stop_timer():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    subject_id = data.get('subject_id')
    duration = data.get('duration')
    
    if not subject_id or not duration:
        return jsonify({'error': 'Missing parameters'}), 400
    
    # Save the study session
    StudySession.create_session(mongo.db, session['user_id'], subject_id, duration)
    
    return jsonify({'success': True, 'message': 'Study session saved'})

@main.route('/api/delete_subject/<subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    result = Subject.delete_subject(mongo.db, subject_id, session['user_id'])
    if result.deleted_count > 0:
        return jsonify({'success': True, 'message': 'Subject deleted'})
    else:
        return jsonify({'error': 'Subject not found'}), 404

def calculate_streak(mongo_db, user_id):
    # Simplified streak calculation using datetime
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    streak = 0
    
    for i in range(30):  # Check last 30 days
        check_date = today - timedelta(days=i)
        sessions = list(mongo_db.study_sessions.find({
            'user_id': ObjectId(user_id),
            'session_date': check_date
        }))
        
        if sessions and any(s['duration_minutes'] > 0 for s in sessions):
            streak += 1
        else:
            break
    
    return streak

def prepare_chart_data(subjects, sessions):
    # Prepare data for Chart.js
    subject_names = [subject['name'] for subject in subjects]
    subject_times = [0] * len(subjects)
    
    subject_id_to_index = {str(subject['_id']): i for i, subject in enumerate(subjects)}
    
    for session in sessions:
        subject_id = str(session['subject_id'])
        if subject_id in subject_id_to_index:
            index = subject_id_to_index[subject_id]
            subject_times[index] += session['duration_minutes'] / 60  # Convert to hours
    
    return {
        'subject_names': subject_names,
        'subject_times': subject_times,
        'subject_colors': [subject['color'] for subject in subjects]
    }

@main.route('/api/dashboard_stats')
def dashboard_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    # Get today's sessions
    today_sessions = StudySession.get_today_sessions(mongo.db, user_id)
    total_today_minutes = sum(session['duration_minutes'] for session in today_sessions)
    today_hours = round(total_today_minutes / 60, 1)
    
    # Get weekly sessions
    weekly_sessions = StudySession.get_weekly_sessions(mongo.db, user_id)
    weekly_hours = round(sum(session['duration_minutes'] for session in weekly_sessions) / 60, 1)
    
    # Get subjects and calculate progress
    subjects = Subject.get_user_subjects(mongo.db, user_id)
    subject_progress = []
    
    for subject in subjects:
        subject_sessions = [s for s in today_sessions if str(s['subject_id']) == str(subject['_id'])]
        subject_today_minutes = sum(s['duration_minutes'] for s in subject_sessions)
        daily_goal_minutes = subject.get('weekly_goal_hours', 1) * 60 / 7
        percentage = min(round((subject_today_minutes / daily_goal_minutes) * 100, 1), 100) if daily_goal_minutes > 0 else 0
        
        subject_progress.append({
            'subject_id': str(subject['_id']),
            'today_minutes': subject_today_minutes,
            'percentage': percentage
        })
    
    # Calculate daily goal percentage
    total_daily_goal = sum(subject.get('weekly_goal_hours', 0) for subject in subjects) / 7
    daily_goal_percentage = round((today_hours / total_daily_goal) * 100, 1) if total_daily_goal > 0 else 0
    
    return jsonify({
        'success': True,
        'stats': {
            'today_hours': today_hours,
            'weekly_hours': weekly_hours,
            'subject_count': len(subjects),
            'daily_goal_percentage': daily_goal_percentage,
            'subject_progress': subject_progress
        }
    })