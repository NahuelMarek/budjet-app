import sqlite3
from flask import Flask,  jsonify, request
from flask_cors import CORS
from socket import gethostname

DATABASE = 'budget.db'

def get_db_connection():
    print("Obteniendo conexión...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla 'productos' si no existe
def create_table():
    print("Creando tabla productos...") # Para probar que se ejecuta la función
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            category_id integer PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            balance INTEGER NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deposits (
        deposit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT,
        amount REAL,
        descripcion TEXT NONE,
        FOREIGN KEY (categoria) REFERENCES categorias(categoria)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS withdraws (
        withdraw_id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT,
        amount REAL,
        descripcion TEXT NONE,
        FOREIGN KEY (categoria) REFERENCES categorias(categoria)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


# Verificar si la base de datos existe, si no, crearla y crear la tabla
def create_database():
    print("Creando la BD...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()

# Crear la base de datos y la tabla si no existen
create_database()

#-----------------------------------------------------------------------------------------------------------
class Categorias:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()
        self.balance = 0

    def agregar_categoria(self, categoria):
        producto_existente = self.consultar(categoria)
        if producto_existente:
            return jsonify({'message': 'Ya existe un producto con ese código.'}), 400


     #nuevo_producto = Producto(codigo, descripcion, cantidad, precio)
        self.cursor.execute("INSERT INTO categorias (categoria,balance) VALUES(?,?)", (categoria,0))
        self.conexion.commit()
        return jsonify({'message': 'Producto agregado correctamente.'}), 200

    def consultar(self, categoria):
        self.cursor.execute("SELECT * FROM categorias WHERE categoria = ?", (categoria,))
        row = self.cursor.fetchone()
        if row:
            return True
        return None


    def listar_categorias(self):
        self.cursor.execute("SELECT * FROM categorias")
        rows = self.cursor.fetchall()
        categorias = []

        for row in rows:
            categoria_id, categoria, balance = row

            categoria = {'categoria_id':  categoria_id, 'categoria': categoria, 'balance': balance}
            categorias.append(categoria)
        return jsonify(categorias), 200

    def deposit(self, categoria, amount, description):
        categoria_existente = self.consultar(categoria)
        if categoria_existente:
            self.cursor.execute("INSERT INTO deposits (categoria, amount, descripcion) VALUES (?, ?, ?)", (categoria, amount, description))
            self.conexion.commit()
            self.cursor.execute("UPDATE categorias SET balance = balance + ? WHERE categoria = ?", (amount, categoria,))
            self.conexion.commit()
            return jsonify({'message': 'deposito agregado correctamente.'}), 200
        else:
            return jsonify({'message': 'no existe la categoria.'}), 404



    def check_funds(self, categoria, amount):
        self.cursor.execute("SELECT * FROM categorias WHERE categoria = ?", (categoria,))
        row = self.cursor.fetchone()
        balance = row[2]
        if balance >= float(amount):
            return True
        return jsonify({'message': 'Cantidad de dinero disponible insuficiente.'}), 400



    def withdraw(self, categoria, amount, description):
        categoria_existente = self.consultar(categoria)
        if categoria_existente:
            if self.check_funds(categoria, amount):
                self.cursor.execute("INSERT INTO withdraws (categoria, amount, descripcion) VALUES (?, ?, ?)", (categoria, amount, description))
                self.conexion.commit()
                self.cursor.execute("UPDATE categorias SET balance = balance - ? WHERE categoria = ?", (amount, categoria))
                self.conexion.commit()
                return jsonify({'message': 'retiro realizado correctamente.'}), 200
            else:
                return jsonify({'message': 'no existe la categoria.'}), 404
#---------------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)

categorias = Categorias()

@app.route('/listado', methods=['GET'])
def obtener_categorias():
    return categorias.listar_categorias()

@app.route('/categorias', methods=['POST'])
def agregar_categoria():
    categoria = request.json.get('categoria')
    return categorias.agregar_categoria(categoria)

@app.route('/depositos', methods=['POST'])
def agregar_deposito():
    categoria = request.json.get('categoria')
    amount = request.json.get('amount')
    descripcion = request.json.get('descripcion')
    return categorias.deposit(categoria,amount,descripcion)

@app.route('/withdraws', methods=['POST'])
def agregar_withdraw():
    categoria = request.json.get('categoria')
    amount = request.json.get('amount')
    descripcion = request.json.get('descripcion')
    return categorias.withdraw(categoria,amount,descripcion)

@app.route('/')
def index():
    return 'API de Inventario'


# Finalmente, si estamos ejecutando este archivo, lanzamos app.

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run()
#app = Flask(__name__)

git init
git branch -M main
git remote add origin git@github.com:NahuelMarek/budjet-app.git
git push -u origin main