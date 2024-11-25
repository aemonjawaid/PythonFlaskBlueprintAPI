from flask import Blueprint, jsonify, request
from flask.views import MethodView

from ..extensions import db
from ..models.user import User

main = Blueprint('main', __name__)


class Users(MethodView):

    def get(self):
        users = User.query.all()
        user_obj = [
            {
                "id": user.id,
                "name": user.name
            }
            for user in users
        ]

        return jsonify(user_obj), 200

    def post(self):
        req = request.get_json()

        username = req.get("name")
        if not username:
            return jsonify({"message": "name is required"}), 400

        user = User(name=username)
        db.session.add(user)
        db.session.commit()
        return jsonify({"id": user.id}), 201


# Register the Users class as a view for the "/users" URL
main.add_url_rule('/users', view_func=Users.as_view('users'))
