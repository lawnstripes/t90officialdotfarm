from flask import render_template, redirect, request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_refresh_token_required,
                                get_jwt_identity, jwt_optional)
from flask_socketio import emit
from app import app, db, socketio
from app.models import User, Farm


@app.route('/')
@app.route('/index')
def index():
    farms = Farm.get_farm_cnt()
    return render_template('index.html', farms=farms)


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


@app.route('/api/login', methods=['POST'])
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'message': 'missing JSON request'}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    u = User.query.filter_by(username=username).one_or_none()
    if u is not None and u.verify_password(password):
        ret = {
            'access_token': create_access_token(identity=u.username),
            'refresh_token': create_refresh_token(identity=u.username)
        }
        return jsonify(ret), 200
    else:
        return jsonify({'message': 'invalid user/password'}), 200


@app.route('/api/refresh', methods=['POST'])
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@app.route('/api/farms', methods=['GET', 'POST'])
@app.route('/farms', methods=['GET', 'POST'])
@jwt_optional
def farms():
    if request.method == 'GET':
        ret = {
            'farms': Farm.get_farm_cnt()
        }
        return jsonify(ret), 200
    else:
        current_user = get_jwt_identity()
        if current_user is None:
            return jsonify({'message': 'not authenticated'}), 401
        farms = request.json.get('farms', None)
        twitch_user = request.json.get('twitch_user', None)
        f = Farm(twitch_user=twitch_user, farm_cnt=farms)
        db.session.add(f)
        db.session.commit()
        farm_cnt = Farm.get_farm_cnt()
        broadcast_farms(farm_cnt)
        return jsonify({'farms': farm_cnt})


@app.route('/farms/<twitchuser>', methods=['GET'])
@app.route('/api/farms/<twitchuser>', methods=['GET'])
def user_farms(twitchuser):
    pass


@socketio.on('connect')
def connect_farms():
    emit('farms', {'farms': Farm.get_farm_cnt()})


def broadcast_farms(farms):
    socketio.emit('farms', {'farms': farms}, broadcast=True)
