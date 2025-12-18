from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from models import Resource, User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please login.')

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired()])
    start_time = DateTimeLocalField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeLocalField('End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save Event')

    def validate_end_time(self, end_time):
        if self.start_time.data and end_time.data:
            if end_time.data <= self.start_time.data:
                raise ValidationError('End time must be after start time.')

class ResourceForm(FlaskForm):
    name = StringField('Resource Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[
        ('room', 'Room'), 
        ('instructor', 'Instructor'), 
        ('equipment', 'Equipment')
    ], validators=[DataRequired()])
    submit = SubmitField('Save Resource')

class AllocationForm(FlaskForm):
    # Choices will be populated dynamically in the view
    resource_id = SelectField('Resource', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Allocate Resource')
