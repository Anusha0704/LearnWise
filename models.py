from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(300), unique=True, nullable=False)
    is_paid = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Numeric)
    duration = db.Column(db.Numeric)
    level = db.Column(db.String(50))
    subject = db.Column(db.String(100))
    source = db.Column(db.String(100))

class Ratings(db.Model):
    __tablename__ = 'ratings'
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    number_of_ratings = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Numeric, nullable=False)


from flask_login import UserMixin

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hashed
    is_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.user_id)
