
from flask  import Flask, request, jsonify



app = Flask(__name__)

def get_ip(ip):
    pass

def get_weather():
    pass


@app.route('/api/hello'):
def hello():
    visitor_name = request.args.get()
    visitor_ip = request.remote_addr





if __name__ == "__main__":
    app.run(debug=True)