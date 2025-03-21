from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import pymysql
from datetime import timedelta

# Initialize Flask App
app = Flask(__name__)

# Database Configuration (Using MySQL in phpMyAdmin)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10)  # Token expires in 10 minutes

# Initialize Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Product(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Create Database Tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the RESTful API"}), 200

# User Registration
@app.route('/signup', methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json()
    if not data or not all(key in data for key in ['name', 'username', 'password']):
        return jsonify({'message': 'Missing data'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already taken'}), 409

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json()
    if not data or not all(key in data for key in ['username', 'password']):
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Update User
@app.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    current_user_id = get_jwt_identity()
    if str(current_user_id) != str(id):
        return jsonify({"message": "Unauthorized"}), 403
    
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'username' in data:
        user.username = data['username']
    
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

# Product Endpoints
@app.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json()
    if not all(key in data for key in ['pname', 'price', 'stock']):
        return jsonify({'message': 'Missing product details'}), 400
    
    try:
        new_product = Product(
            pname=data['pname'],
            description=data.get('description', ''),
            price=float(data['price']),
            stock=int(data['stock'])
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'}), 201
    except ValueError:
        return jsonify({'message': 'Invalid data type for price or stock'}), 400

@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    return jsonify([{ "id": p.pid, "name": p.pname, "price": p.price, "stock": p.stock } for p in products]), 200

@app.route('/products/<int:pid>', methods=['GET'])
@jwt_required()
def get_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify({
        "id": product.pid,
        "name": product.pname,
        "description": product.description,
        "price": product.price,
        "stock": product.stock
    }), 200

@app.route('/products/<int:pid>', methods=['PUT'])
@jwt_required()
def update_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    data = request.get_json()
    if 'pname' in data:
        product.pname = data['pname']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']
    if 'stock' in data:
        product.stock = data['stock']
    
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'}), 200

@app.route('/products/<int:pid>', methods=['DELETE'])
@jwt_required()
def delete_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
