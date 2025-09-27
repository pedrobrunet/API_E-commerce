from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SECRET_KEY'] = "minha123"

Login_manager = LoginManager()
db = SQLAlchemy(app)
Login_manager.init_app(app)
Login_manager.login_view = 'login'
CORS(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(75), unique=True, nullable=False)
    password = db.Column(db.String(75), nullable=False)
    cart = db.relationship('CartItem', backref='user', lazy=True)

class Product(db.Model):
    # model = caminho bd = (db).Tipo
    # nullable = CAMPO OBRIGATORIO
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

class CartItem(db.Model):
      id = db.Column(db.Integer, primary_key=True)  
      user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
      product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


@Login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=["POST"])
def login():
    data = request.json
   
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and data.get('password') == user.password:
        login_user(user)
        return jsonify({"message":"login successful"})
    return jsonify({"message":"invalid credentials"}), 401    

@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message":"logout successful"})




@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name= data["name"],price= data["price"],description = data["description"])
        db.session.add(product)
        db.session.commit()
        return jsonify({"message":"product accept"})
    return jsonify({"message":"invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    #Recuperar o prod  uto de dados
    #Verificar se o produto existe
    #Se existe, apagar do banco de dados
    #Se não existe, retornar 404 (not found)
    product= Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"product deleted sucessfully"})
    return jsonify({"message":"product not found"}), 404

@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message":"product not found"}), 404

@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    data = request.json
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message":"product not found"}), 404
    data = request.json
    if 'name' in data:
        product.name = data['name']

    if 'price' in data:
        product.price = data['price']

    if 'description' in data:
        product.description = data['description']   

    db.session.commit()    
    return jsonify({"message":"product updated sucessfully"})

@app.route('/api/products', methods=["GET"])
@login_required
def get_products():
   products = Product.query.all()
   product_lista = []  
   for product in products:
       product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            
        }
       product_lista.append(product_data)
   return jsonify(product_lista)

#Checkout
@app.route('/api/cart/add/<int:product_id>', methods=["POST"])
@login_required
def add_to_cart(product_id):
    #user
    user = User.query.get(int(current_user.id))
    #product
    product = Product.query.get(product_id)

    if user and product:
        cart_item = CartItem(user_id=user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        
        return jsonify({"message":"product added to cart"})
    return jsonify({"message":"user or product not found"}), 400
    

if __name__ == "__main__":
    app.run(debug=True)