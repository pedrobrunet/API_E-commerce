from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)
CORS(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(75), unique=True, nullable=False)
    password = db.Column(db.String(75), nullable=False)

class Product(db.Model):
    # model = caminho bd = (db).Tipo
    # nullable = CAMPO OBRIGATORIO
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


@app.route('/login', methods=["POST"])
def login():
    data = request.json
   
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and data.get('password') == user.password:
        return jsonify({"message":"login successful"})
    return jsonify({"message":"invalid credentials"}), 401    


@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name= data["name"],price= data["price"],description = data["description"])
        db.session.add(product)
        db.session.commit()
        return jsonify({"message":"product accept"})
    return jsonify({"message":"invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
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


# / dentro da rota significa pagina inicial 
@app.route('/')
def hello_word() :
    return 'hello world'

if __name__ == "__main__":
    app.run(debug=True)