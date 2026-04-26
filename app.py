from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "v1 - App is running fine!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)