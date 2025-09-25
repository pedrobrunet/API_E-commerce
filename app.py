from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

class Product(db.Model):
    # model = caminho bd = (db).Tipo
    # nullable = CAMPO OBRIGATORIO
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

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
    #Recuperar o produto de dados
    #Verificar se o produto existe
    #Se existe, apagar do banco de dados
    #Se não existe, retornar 404 (not found)
    product= Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"product deleted sucessfully"})
    return jsonify({"message":"product not found"}), 404
# / dentro da rota significa pagina inicial 
@app.route('/')
def hello_word() :
    return 'hello world'

if __name__ == "__main__":
    app.run(debug=True)