from app import app
from app.models import FarmModel


@app.shell_context_processor
def make_shell_context():
    return {'FarmModel': FarmModel}


if __name__ == "__main__":
    app.run()
