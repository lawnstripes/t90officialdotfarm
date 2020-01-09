from flask import render_template, jsonify, redirect
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


@app.route('/farm')
def farms():
    return jsonify(count=42)
