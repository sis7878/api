from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from models import db, Pizza
from routes import pizza_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)


    jwt = JWTManager(app)


    app.register_blueprint(pizza_bp, url_prefix='/api/pizza')


    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()

        if not data or not 'username' in data or not 'password' in data:
            return jsonify({"msg": "Missing username or password"}), 400

        username = data['username']
        password = data['password']


        if username != 'admin' or password != 'password':  
            return jsonify({"msg": "Bad username or password"}), 401


        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return jsonify(access_token=access_token, refresh_token=refresh_token)


    @app.route('/logout', methods=['DELETE'])
    @jwt_required()
    def logout():
        return jsonify({"msg": "Successfully logged out"}), 200


    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
