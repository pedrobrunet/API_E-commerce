from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

class product(db.Model):
    # model = caminho bd = (db).Tipo
    # nullable = CAMPO OBRIGATORIO
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)



# / dentro da rota significa pagina inicial 
@app.route('/')
def hello_word() :
    return 'hello world'

if __name__ == "__main__":
    app.run(debug=True)