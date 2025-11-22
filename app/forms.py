from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from datetime import datetime

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(max=100)])
    color = SelectField('Color', choices=[
        ('#6366F1', 'Indigo'),
        ('#8B5CF6', 'Violet'),
        ('#10B981', 'Emerald'),
        ('#F59E0B', 'Amber'),
        ('#EF4444', 'Red'),
        ('#3B82F6', 'Blue'),
        ('#06B6D4', 'Cyan'),
        ('#84CC16', 'Lime')
    ], default='#6366F1')
    icon = SelectField('Icon', choices=[
        ('📚', 'Books'),
        ('🧠', 'Brain'),
        ('🔬', 'Science'),
        ('∫', 'Math'),
        ('α', 'Alpha'),
        ('📖', 'Book'),
        ('✏️', 'Pencil'),
        ('📊', 'Chart')
    ], default='📚')
    weekly_goal_hours = IntegerField('Weekly Goal (hours)', 
                                   validators=[DataRequired(), NumberRange(min=1, max=50)],
                                   default=5)
    submit = SubmitField('Add Subject')

class GoalForm(FlaskForm):
    title = StringField('Goal Title', validators=[DataRequired(), Length(max=200)])
    description = StringField('Description', validators=[Length(max=500)])
    target_date = DateField('Target Date', validators=[DataRequired()], default=datetime.utcnow)
    submit = SubmitField('Create Goal')