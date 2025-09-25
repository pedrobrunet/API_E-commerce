from flask import Flask, request
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
    product = Product(name= data["name"],price= data["price"],description = data["description"])
    db.session.add(product)
    db.session.commit()
    return "Cadastrado com sucesso"

# / dentro da rota significa pagina inicial 
@app.route('/')
def hello_word() :
    return 'hello world'

if __name__ == "__main__":
    app.run(debug=True)