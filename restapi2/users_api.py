from flask_restful import abort, Resource
from data import db_session
from flask import jsonify
from data.users import User
from user_parser import parser



def get_or_abort_if_user_not_found(session, user_id):
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
    return user


class UsersResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        user = get_or_abort_if_user_not_found(session, user_id)
        return jsonify(
            {
                'user': user.to_dict(max_serialization_depth=0),
            }
        )

    def delete(self, user_id):
        session = db_session.create_session()
        user = get_or_abort_if_user_not_found(session, user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': "OK"})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {
                'users': [user.to_dict(rules=('-hashed_password'), max_serialization_depth=0,
                                       only=['id', 'email', 'name', 'surname']
                                       ) for user in users]
            }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(name = args['name'],
                    surname = args['surname'],
                    email = args['email'],
                    age = args['age'],
                    position = args['position'],
                    speciality = args['speciality'],
                    address = args['address'],
                    )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})
