from flask import Flask, request, jsonify
import sqlite3

from pubsub import AsyncConn

app = Flask(__name__)
pubnub = AsyncConn("Flask Application", "meu_canal")

# Função para conectar ao banco de dados SQLite
def connect_db():
    return sqlite3.connect('data.db')

# Função para criar a tabela se não existir
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tag TEXT NOT NULL,
            permissao INTEGER NOT NULL)
        """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS acesso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            data DATETIME DEFAULT CURRENT_TIMESTAMP,
            resultado TEXT NOT NULL)
        """
    )
    conn.commit()
    conn.close()

# Inicializa a tabela ao iniciar o aplicativo
create_table()

@app.route('/user', methods=['POST'])
def post_user():
    try:
            # ====== POST ==========================================================================
        if request.method == "POST":
            nome = request.json.get('nome')  # Recebe o valor do corpo da requisição JSON
            tag = request.json.get('tag')
            permissao = request.json.get('permissao')
        
            if nome is None:
                return jsonify({"error": "No value provided"}), 400
        
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO user (nome, tag, permissao) VALUES (?, ?, ?)', (nome, tag, permissao))
                conn.commit()
            
            return jsonify({"message": "Usuario cadastrado com sucesso"}), 201

        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/acesso', methods=['POST'])
def post_acesso():
    try:
        if request.method == 'POST':
            tag = request.json.get('tag')

            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, permissao FROM user WHERE tag=?',(tag,))
                result = cursor.fetchone()
                if result:
                    id_user, permissao = result
                    if permissao == 1:
                        resultado = "Acesso Permitido"
                        cursor.execute('INSERT INTO acesso (id_user, resultado) VALUES (?, ?)', (id_user, resultado))
                        conn.commit()
                    else:
                        resultado = "Acesso Negado"
                        cursor.execute('INSERT INTO acesso (id_user, resultado) VALUES (?, ?)', (id_user, resultado))
                        conn.commit()
                else:
                    resultado = "Acesso Negado, Usuário Desconhecido"
                    cursor.execute('INSERT INTO acesso (id_user, resultado) VALUES (?, ?)', (999, resultado))
                    conn.commit()
                
            get_ultimo_acesso()
                
            return jsonify({"message": "Tentativa de acesso gravada"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user', methods=['GET'])
def get_users():
    try:
            # ====== GET ==========================================================================
        if request.method == "GET":
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user")
                usuarios = cursor.fetchall()

            return jsonify(usuarios), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/acesso', methods=['GET'])
def get_acesso():
    try:
            # ====== GET ==========================================================================
        if request.method == "GET":
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM acesso")
                acessos = cursor.fetchall()

            return jsonify(acessos), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_ultimo_acesso():
    try:
            # ====== GET ==========================================================================
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM acesso ORDER BY id DESC LIMIT 1")
            ultimo_acesso = cursor.fetchall()

        pubnub.publish(ultimo_acesso)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user', methods = ['DELETE'])
def delete_user():
    try:
        if request.method == "DELETE":
            id = request.json.get('id')
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM user WHERE id=?",(id))

            return jsonify({"message": "Usuario excluido"}), 201 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user', methods = ["PUT"])
def update_user():
    try:
        if request.method == "PUT":
            id = request.json.get('id')
            permissao = request.json.get('permissao')
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE user SET permissao = ? WHERE id=?', (permissao, id))

            return jsonify({"message": "Permissao do usuario alterada"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
