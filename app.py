from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database

db = SQLAlchemy(app)
CORS(app)

# Define a Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"Customer('{self.name}', '{self.email}')"

# Create the database and tables
with app.app_context():
    db.create_all()

# Define a route to add a new customer
@app.route('/customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'])
    db.session.add(new_customer)
    db.session.flush()  # Ensure data is written to the DB
    db.session.refresh(new_customer)  # Refresh to get the latest state
    db.session.commit()
    return jsonify({"message": "Customer added successfully"}), 201

# Define a route to get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    db.session.expire_all()  # Ensure all objects are expired
    customers = Customer.query.all()
    customers_list = [{"id": customer.id, "name": customer.name, "email": customer.email} for customer in customers]
    return jsonify(customers_list)

if __name__ == '__main__':
    app.run(debug=True)
