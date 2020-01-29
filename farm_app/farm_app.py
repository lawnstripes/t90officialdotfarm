from app import app, Config, socketio, db
from app.models import Farm, User
import click


@app.shell_context_processor
def make_shell_context():
    return {'FarmModel': Farm, 'Config': Config}


@app.cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.cli.command("init_db")
@click.argument("user", envvar="FARM_BOT_USER")
@click.argument("password", envvar="FARM_BOT_PW")
def init_db(user, password):
    u = User(username=user)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=True)
