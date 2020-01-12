from app import app, Config, socketio
from app.models import Farm


@app.shell_context_processor
def make_shell_context():
    return {'FarmModel': Farm, 'Config': Config}


if __name__ == "__main__":
    socketio.run(app)
