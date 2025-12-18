from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, Event, Resource, EventResourceAllocation, User
from forms import EventForm, ResourceForm, AllocationForm, LoginForm, SignupForm
from utils.conflict_checker import is_resource_available
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scheduler.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ensure DB tables exist
with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    if not current_user.is_authenticated:
        return render_template('landing.html')
        
    total_events = Event.query.count()
    total_resources = Resource.query.count()
    recent_events = Event.query.order_by(Event.start_time.desc()).limit(5).all()
    return render_template('dashboard.html', total_events=total_events, total_resources=total_resources, recent_events=recent_events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('auth/signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dashboard'))

# --- Event Routes ---
@app.route('/events')
@login_required
def event_list():
    events = Event.query.order_by(Event.start_time).all()
    return render_template('events/list.html', events=events)

@app.route('/events/new', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            description=form.description.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('event_list'))
    return render_template('events/create.html', form=form)

@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.description = form.description.data
        
        # Check conflicts for existing allocations
        # If time changed, we must re-validate all existing allocations for this event
        allocations = EventResourceAllocation.query.filter_by(event_id=event.id).all()
        conflict_found = False
        for alloc in allocations:
            available, reason = is_resource_available(alloc.resource_id, event.start_time, event.end_time, exclude_event_id=event.id)
            if not available:
                flash(f'Cannot update time: {reason}', 'danger')
                conflict_found = True
                break
        
        if not conflict_found:
            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('event_list'))
            
    return render_template('events/edit.html', form=form, event=event)

# --- Resource Routes ---
@app.route('/resources')
@login_required
def resource_list():
    resources = Resource.query.all()
    return render_template('resources/list.html', resources=resources)

@app.route('/resources/new', methods=['GET', 'POST'])
@login_required
def create_resource():
    form = ResourceForm()
    if form.validate_on_submit():
        resource = Resource(name=form.name.data, type=form.type.data)
        db.session.add(resource)
        try:
            db.session.commit()
            flash('Resource created successfully!', 'success')
            return redirect(url_for('resource_list'))
        except:
            db.session.rollback()
            flash('Resource name must be unique.', 'danger')
    return render_template('resources/create.html', form=form)

# --- Allocation Routes ---
@app.route('/allocations/allocate', methods=['GET', 'POST'])
def allocate_resource():
    # If event_id provided via query param
    event_id = request.args.get('event_id')
    event = Event.query.get(event_id) if event_id else None
    
    form = AllocationForm()
    # Populate resources
    form.resource_id.choices = [(r.id, f"{r.name} ({r.type})") for r in Resource.query.all()]
    
    if request.method == 'POST':
        # If submitting, we might need event_id from hidden field or logical flow
        # Simplification: The form is processed differently if we had a pure allocation page
        # But let's assume we pass event_id in query or select it.
        # For this requirement, let's make a dedicated page that selects BOTH or just resource if event is known.
        # Let's support: select Event then select Resource? Or just "Allocate to THIS event"
        
        # Let's adjust to be simpler: "Allocate Resource to Event X"
        # We need event_id.
        pass

    # Alternative Route Design: /events/<id>/allocate
    return render_template('allocations/allocate.html', form=form, events=Event.query.all()) 

@app.route('/events/<int:event_id>/allocate', methods=['GET', 'POST'])
def allocate_to_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = AllocationForm()
    # Populate resources
    form.resource_id.choices = [(r.id, f"{r.name} ({r.type})") for r in Resource.query.all()]
    
    if form.validate_on_submit():
        resource_id = form.resource_id.data
        
        # Check for duplicates
        existing = EventResourceAllocation.query.filter_by(event_id=event.id, resource_id=resource_id).first()
        if existing:
            flash('Resource already allocated to this event.', 'warning')
            return redirect(url_for('allocate_to_event', event_id=event.id))
            
        # Check Conflict
        available, reason = is_resource_available(resource_id, event.start_time, event.end_time)
        if not available:
            flash(f'Conflict Detected: {reason}', 'danger')
        else:
            allocation = EventResourceAllocation(event_id=event.id, resource_id=resource_id)
            db.session.add(allocation)
            db.session.commit()
            flash('Resource allocated successfully!', 'success')
            return redirect(url_for('event_list'))
            
    return render_template('allocations/allocate.html', form=form, event=event)


# --- Reports ---
@app.route('/reports', methods=['GET', 'POST'])
def reports():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    report_data = []
    
    if start_date and end_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        # For each resource, calculate utilization
        resources = Resource.query.all()
        for r in resources:
            # Get allocations for this resource within range
            # Allocations -> Event
            allocs = db.session.query(Event).join(EventResourceAllocation).filter(
                EventResourceAllocation.resource_id == r.id,
                Event.start_time >= start_dt,
                Event.end_time <= end_dt
            ).all()
            
            total_seconds = 0
            for e in allocs:
                total_seconds += (e.end_time - e.start_time).total_seconds()
            
            total_hours = total_seconds / 3600
            report_data.append({
                'resource': r.name,
                'hours': round(total_hours, 2),
                'bookings': len(allocs)
            })
            
    return render_template('reports/utilization.html', report_data=report_data, start_date=start_date, end_date=end_date)
    
if __name__ == '__main__':
    app.run(debug=True)
