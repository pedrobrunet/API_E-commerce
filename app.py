from flask import Flask

app = Flask(__name__)

# Definindo a rota raiz (pagina inicial) e a função que sera realizada ao executar 

# / dentro da rota significa pagina inicial 
@app.route('/')

def hello_word() :
    return 'hello world'

if __name__ == "__main__":
    app.run(debug=True)