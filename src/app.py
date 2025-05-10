from flask import Flask
from src.api.tasks import tasks_blueprint

app = Flask(__name__)
app.register_blueprint(tasks_blueprint)

@app.route('/')
def health_check():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)