import os
from http import HTTPStatus
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config.from_object(os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# this import cannot be moved due to cyclic import dependencies
from models import Book


@app.route("/")
def hello():
    return jsonify(message="Hello World - output to is!!")


def _add_book(**kwargs):
    try:
        book = Book(**kwargs)
        db.session.add(book)
        db.session.commit()
        return jsonify(message="Book added. book id={}".format(book.id))
    except Exception as e:
        return jsonify(errors=str(e)), HTTPStatus.BAD_REQUEST


def _jsonify_book_not_found(book_id):
    return jsonify(errors="Book not found. book id={}".format(book_id)), \
           HTTPStatus.NOT_FOUND


@app.route("/book", methods=['POST'])
def add_book():
    field_data = request.json
    if not field_data:
        return jsonify(errors=('Missing request JSON and/or content header:'
                               ' -H Content-Type:application/json')), \
               HTTPStatus.BAD_REQUEST
    return _add_book(**field_data)


@app.route("/book/<book_id>", methods=['PUT'])
def update_book(book_id):
    field_data = request.json
    if not field_data:
        return jsonify(errors=('Missing request JSON and/or content header:'
                               ' -H Content-Type:application/json')), \
               HTTPStatus.BAD_REQUEST
    book = Book.query.filter_by(id=book_id).first()
    if book:
        Book.query.filter_by(id=book_id).update(field_data)
        db.session.commit()
        return jsonify(data=book.serialize())
    else:
        return _jsonify_book_not_found(book_id)


@app.route("/book/<book_id>", methods=['DELETE'])
def delete_book(book_id):
    try:
        book = Book.query.filter_by(id=book_id).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify(message="Book deleted. book id={}".format(book.id))
        else:
            return _jsonify_book_not_found(book_id)
    except Exception as e:
        return jsonify(errors=str(e)), HTTPStatus.BAD_REQUEST


@app.route("/book/getall", methods=['GET'])
def get_all():
    try:
        books = Book.query.all()
        return jsonify(data=[e.serialize() for e in books])
    except Exception as e:
        return jsonify(errors=str(e)), HTTPStatus.BAD_REQUEST


@app.route("/book/<book_id>", methods=['GET'])
def get_by_id(book_id):
    try:
        book = Book.query.filter_by(id=book_id).first()
        if book:
            return jsonify(data=book.serialize())
        else:
            return _jsonify_book_not_found(book_id)
    except Exception as e:
        return jsonify(errors=str(e)), HTTPStatus.BAD_REQUEST


@app.route("/book/form", methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        form_data = request.form
        if not form_data:
            return jsonify(errors='Missing request urlencoded form data.'), \
                   HTTPStatus.BAD_REQUEST
        else:
            return _add_book(**form_data)
    else:
        return render_template("getdata.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
