from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def hello():
    if request.method == 'DELETE':
        return "Метод Запиту Delete"
    return "Метод запиту Get"

@app.route('/get')
def get_data():
    data = request.args.get('data')
    return data

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["name"]
        return f"Ім'я користувача {username}"
    return render_template("login.html")

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    return jsonify({"data": data})

if __name__ == '__main__':
    app.run(debug=True)