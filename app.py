# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///postpartum_health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_physician = db.Column(db.Boolean, default=False)
    weeks_postpartum = db.Column(db.Integer)
    delivery_date = db.Column(db.DateTime)

class DailyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    mental_health = db.Column(db.Integer)
    stress_level = db.Column(db.Integer)
    social_support = db.Column(db.Integer)
    physical_health = db.Column(db.Integer)
    nutrition = db.Column(db.Integer)
    sleep_hours = db.Column(db.Float)
    sleep_quality = db.Column(db.Integer)
    economic_stress = db.Column(db.Integer)
    hormonal_changes = db.Column(db.Boolean)
    notes = db.Column(db.Text)

class EPDSScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    score = db.Column(db.Integer, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Helper functions
def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorator

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=24)},
                           app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/daily_log', methods=['POST'])
@token_required
def create_daily_log(current_user):
    data = request.json
    new_log = DailyLog(user_id=current_user.id, date=datetime.now().date(), **data)
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'message': 'Daily log created successfully'}), 201

@app.route('/daily_log', methods=['GET'])
@token_required
def get_daily_logs(current_user):
    logs = DailyLog.query.filter_by(user_id=current_user.id).all()
    return jsonify([{column.name: getattr(log, column.name) for column in log.__table__.columns} for log in logs])

@app.route('/epds', methods=['POST'])
@token_required
def create_epds_score(current_user):
    data = request.json
    new_score = EPDSScore(user_id=current_user.id, date=datetime.now().date(), score=data['score'])
    db.session.add(new_score)
    db.session.commit()
    return jsonify({'message': 'EPDS score recorded successfully'}), 201

@app.route('/epds', methods=['GET'])
@token_required
def get_epds_scores(current_user):
    scores = EPDSScore.query.filter_by(user_id=current_user.id).all()
    return jsonify([{column.name: getattr(score, column.name) for column in score.__table__.columns} for score in scores])

@app.route('/message', methods=['POST'])
@token_required
def send_message(current_user):
    data = request.json
    new_message = Message(sender_id=current_user.id, receiver_id=data['receiver_id'], content=data['content'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully'}), 201

@app.route('/messages', methods=['GET'])
@token_required
def get_messages(current_user):
    messages = Message.query.filter((Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)).all()
    return jsonify([{column.name: getattr(message, column.name) for column in message.__table__.columns} for message in messages])

@app.route('/profile', methods=['GET', 'PUT'])
@token_required
def profile(current_user):
    if request.method == 'GET':
        return jsonify({column.name: getattr(current_user, column.name) for column in current_user.__table__.columns if column.name != 'password_hash'})
    elif request.method == 'PUT':
        data = request.json
        for key, value in data.items():
            setattr(current_user, key, value)
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)