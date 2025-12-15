from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    print("🚀 Starting minimal Flask app...")
    app.run(port=5002, debug=False)
