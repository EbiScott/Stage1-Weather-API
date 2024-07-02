
from flask  import Flask, request, jsonify



app = Flask(__name__)

def get_ip():
    pass

def get_weather():
    pass


@app.route('/'):
def first_endpoint():
    return 






if __name__ == "__main__":
    app.run(debug=True)