from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to CCA CI/CD Deployment - Version 2 Updated!",
        "status": "success",
        "version": "v2.0"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)