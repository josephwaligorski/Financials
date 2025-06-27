# backend/app.py
# This is the main Flask application file.
# It defines the API endpoints to interact with the financial data stored in SQLite.

import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# --- App Setup ---
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# --- Database Configuration ---
# Create a 'data' directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(data_dir, "finance.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Models ---
class GhlEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100))
    service = db.Column(db.String(100))
    clients = db.Column(db.Float)
    rate = db.Column(db.Float)
    multiplier = db.Column(db.Float)

class StripeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(100))
    type = db.Column(db.String(50))
    transactions = db.Column(db.Float)
    price = db.Column(db.Float)

class ExpenseEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    item = db.Column(db.String(100))
    cost = db.Column(db.Float)

# --- Helper to convert model to dict ---
def to_dict(instance):
    return {c.name: getattr(instance, c.name) for c in instance.__table__.columns}

# --- API Endpoints ---

# ADDED: Healthcheck endpoint for Docker to verify the app is running.
@app.route('/health')
def health_check():
    """Confirms the app is alive."""
    return "OK", 200

@app.route('/api/data', methods=['GET'])
def get_all_data():
    """Fetches all data from the database."""
    with app.app_context():
        ghl_data = [to_dict(entry) for entry in GhlEntry.query.all()]
        stripe_data = [to_dict(entry) for entry in StripeEntry.query.all()]
        expense_data = [to_dict(entry) for entry in ExpenseEntry.query.all()]
    return jsonify({
        'ghl': ghl_data,
        'stripe': stripe_data,
        'expenses': expense_data
    })

@app.route('/api/data', methods=['POST'])
def update_all_data():
    """Receives all data from the frontend and updates the database."""
    data = request.json
    
    with app.app_context():
        # Clear existing data
        db.session.query(GhlEntry).delete()
        db.session.query(StripeEntry).delete()
        db.session.query(ExpenseEntry).delete()

        # Add new data from payload, ensuring 'id' is not passed to the constructor
        for item in data.get('ghl', []):
            item.pop('id', None)
            db.session.add(GhlEntry(**item))
        for item in data.get('stripe', []):
            item.pop('id', None)
            db.session.add(StripeEntry(**item))
        for item in data.get('expenses', []):
            item.pop('id', None)
            db.session.add(ExpenseEntry(**item))
            
        db.session.commit()
        
    return jsonify({'message': 'Data saved successfully'}), 200

# --- Database Initialization ---
def initialize_database():
    """Creates database tables and populates with initial data if empty."""
    with app.app_context():
        db.create_all()
        # Check if DB is empty before seeding
        if not GhlEntry.query.first() and not StripeEntry.query.first() and not ExpenseEntry.query.first():
            initial_ghl_data = [
                { 'source': 'Client A', 'service': 'Agency Unlimited', 'clients': 1, 'rate': 297.00, 'multiplier': 1.5 },
                { 'source': 'Client B', 'service': 'Agency Starter', 'clients': 1, 'rate': 97.00, 'multiplier': 1 },
            ]
            initial_stripe_data = [
                { 'service': 'Website Setup', 'type': 'One-Time', 'transactions': 3, 'price': 1500.00 },
                { 'service': 'SEO Subscription', 'type': 'Recurring', 'transactions': 10, 'price': 500.00 },
            ]
            initial_expenses_data = [
                { 'category': 'Software', 'item': 'Google Workspace', 'cost': 12.00 },
                { 'category': 'Marketing', 'item': 'Facebook Ads', 'cost': 1000.00 },
            ]
            for item in initial_ghl_data: db.session.add(GhlEntry(**item))
            for item in initial_stripe_data: db.session.add(StripeEntry(**item))
            for item in initial_expenses_data: db.session.add(ExpenseEntry(**item))
            db.session.commit()

# Create tables when the app starts
initialize_database()

if __name__ == '__main__':
    app.run()
