from flask import Flask, request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'NpmFmMxjmSXk46k'
app.config['MYSQL_DATABASE_DB'] = 'ac03'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.2'
mysql.init_app(app)


@app.route('/')
def welcome():
    return "Microservice User"


@app.route('/signup', methods=['POST'])
def post():
    try:
        _name = request.form['name']
        _email = request.form['email']
        _password = request.form['password']

        if _name and _password and _email:
            conn = mysql.connect()
            cursor = conn.cursor()

            sql = "INSERT INTO tb_users(name, email, password) VALUES (%s, %s, %s)"
            value = (_name, _email, _password)

            cursor.execute(sql, value)
            conn.commit()

            response = jsonify({'message': 'Usuário criado com sucesso!'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except Exception as e:
        print("Problem inserting into db: " + str(e))


@app.route('/list', methods=['GET'])
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    query = 'SELECT name, email, password FROM tb_users'
    cursor.execute(query)

    data = cursor.fetchall()

    response = jsonify({'users': data})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5050)
