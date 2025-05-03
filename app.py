from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Courses, Ratings, Users
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'anusha_girish_adt_project_2025'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('home.html')  # A simple page with Login/Signup options

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = Users(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()

        if user:
            if user.is_admin:
                # Handle un-hashed admin password (see below)
                if user.password == password:
                    login_user(user)
                    flash('Admin Login Successful!')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Invalid admin password.')
            else:
                # Regular user with hashed password
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user)
                    flash('Login Successful!')
                    return redirect(url_for('index'))
                else:
                    flash('Invalid email or password.')
        else:
            flash('User not found.')

    return render_template('login.html')


# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/template')
@login_required
def template_page():
    return render_template('template.html')

from sqlalchemy import asc, desc

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    search_title = request.args.get('title', '')
    platform = request.args.get('platform', '')
    category = request.args.get('category', '')
    sort_duration = request.args.get('sort_duration', '')
    sort_price = request.args.get('sort_price', '')
    sort_rating = request.args.get('sort_rating', '')

    query = db.session.query(
    Courses,
    (db.session.query(Ratings.rating)
        .filter(Ratings.course_id == Courses.id)
        .limit(1)
        .as_scalar()
    ).label('rating'),
    (db.session.query(Ratings.number_of_ratings)
        .filter(Ratings.course_id == Courses.id)
        .limit(1)
        .as_scalar()
    ).label('num_ratings')
    )


    if search_title:
        query = query.filter(Courses.title.ilike(f'%{search_title}%'))
    if platform:
        query = query.filter(Courses.source == platform)
    if category:
        query = query.filter(Courses.subject == category)

    if sort_duration == 'asc':
        query = query.order_by(asc(Courses.duration))
    elif sort_duration == 'desc':
        query = query.order_by(desc(Courses.duration))

    if sort_price == 'asc':
        query = query.order_by(asc(Courses.price))
    elif sort_price == 'desc':
        query = query.order_by(desc(Courses.price))

    if sort_rating == 'asc':
        query = query.order_by(asc('rating'))
    elif sort_rating == 'desc':
        query = query.order_by(desc('rating'))

    courses_with_ratings = query.all()

    platforms = db.session.query(Courses.source).distinct().all()
    categories = db.session.query(Courses.subject).distinct().all()

    return render_template('index.html', 
                           courses_with_ratings=courses_with_ratings, 
                           platforms=platforms,
                           categories=categories,
                           search_title=search_title,
                           selected_platform=platform,
                           selected_category=category,
                           sort_duration=sort_duration,
                           sort_price=sort_price,
                           sort_rating=sort_rating)


@app.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        is_paid = request.form['is_paid'] == 'True'
        price = request.form['price']
        duration = request.form['duration']
        level = request.form['level']
        subject = request.form['subject']
        source = request.form['source']
        initial_rating = float(request.form['initial_rating'])

        existing_course = Courses.query.filter_by(title=title, url=url).first()
        if existing_course:
            flash('Course already exists.')
            return redirect(url_for('add_course'))

        # Add the course (without published)
        new_course = Courses(
            title=title,
            url=url,
            is_paid=is_paid,
            price=price,
            duration=duration,
            level=level,
            subject=subject,
            source=source
        )
        db.session.add(new_course)
        db.session.commit()

        new_rating = Ratings(
            course_id=new_course.id,
            number_of_ratings=1,
            rating=initial_rating
        )
        db.session.add(new_rating)
        db.session.commit()

        flash('Course and initial rating added successfully!')
        return redirect(url_for('index'))

    return render_template('add_course.html')



@app.route('/add_rating', methods=['GET', 'POST'])
@login_required
def add_rating():
    if request.method == 'POST':
        if 'search' in request.form:
            search_title = request.form['search_title']
            matching_courses = Courses.query.filter(Courses.title.ilike(f'%{search_title}%')).all()
            return render_template('add_rating.html', courses=matching_courses, search_title=search_title)

        elif 'submit_rating' in request.form:
            course_id = request.form['course_id']
            user_rating = float(request.form['rating'])

            course = Courses.query.get(course_id)
            if not course:
                flash('Course not found.')
                return redirect(url_for('add_rating'))

            rating_entry = Ratings.query.filter_by(course_id=course.id).first()

            if rating_entry:
                old_total = float(rating_entry.rating) * rating_entry.number_of_ratings
                rating_entry.number_of_ratings += 1
                rating_entry.rating = (old_total + user_rating) / rating_entry.number_of_ratings
                db.session.commit()
                flash(f'Rating updated for {course.title}!')
            else:
                flash('No rating entry found for this course.')

            return redirect(url_for('index'))

    return render_template('add_rating.html', courses=[])


@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('index'))

    if request.method == 'POST':
        course_id = request.form['course_id']
        course = Courses.query.get(course_id)

        if 'update' in request.form and course:
            course.title = request.form['title']
            course.url = request.form['url']
            course.is_paid = request.form['is_paid'] == 'True'
            course.price = request.form['price']
            course.duration = request.form['duration']
            course.level = request.form['level']
            course.subject = request.form['subject']
            course.source = request.form['source']

            # Fetch existing rating record or create new if it doesn't exist
            rating_entry = Ratings.query.filter_by(course_id=course.id).first()
            if not rating_entry:
                rating_entry = Ratings(course_id=course.id)

            rating_entry.rating = request.form.get('rating', type=float)
            rating_entry.number_of_ratings = request.form.get('number_of_ratings', type=int)
            db.session.add(rating_entry) 
            db.session.commit()

            flash('Course updated successfully!')


        elif 'delete' in request.form and course:
            Ratings.query.filter_by(course_id=course.id).delete()
            db.session.delete(course)
            db.session.commit()
            flash('Course and its rating deleted successfully!')

        return redirect(url_for('admin_dashboard'))

    search_title = request.args.get('search_title', '')

    query = db.session.query(
        Courses,
        Ratings.number_of_ratings,
        Ratings.rating
    ).outerjoin(Ratings, Courses.id == Ratings.course_id)

    if search_title:
        query = query.filter(Courses.title.ilike(f'%{search_title}%'))

    courses_with_ratings = query.limit(50).all()

    return render_template('admin_dashboard.html', courses_with_ratings=courses_with_ratings, search_title=search_title)



if __name__ == '__main__':
    app.run(debug=True)

"""
# Main page (after login)
@app.route('/index')
@login_required
def index():
    courses_with_ratings = db.session.query(
        Courses,
        (db.session.query(Ratings.rating)
         .filter(Ratings.course_id == Courses.id)
         .limit(1)
         .as_scalar()
        ).label('rating')
    ).all()
    return render_template('index.html', courses_with_ratings=courses_with_ratings)
"""