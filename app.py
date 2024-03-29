from flask import Flask, send_from_directory
from controllers.chat_controller import chatBot_controller
from models.model import create_model_table
from models.user import create_connection, create_user_table
from helpers.jwt_helper import auth_token
from controllers.user_controllers import register, login, get_user_data, update_user_data, update_password
import os
from dotenv import load_dotenv
from controllers.model_controller import classify_image

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

conn = create_connection()
create_user_table(conn)
create_model_table(conn)


@app.route('/register', methods=['POST'])
def register_api(): return register(app)


@app.route('/login', methods=['POST'])
def login_api(): return login(app)


@app.route('/user-data', methods=['GET'])
@auth_token
def get_user_data_api(email): return get_user_data(email)


@app.route('/update-user-data', methods=['PUT'])
@auth_token
def update_user_data_api(email): return update_user_data(email)


@app.route('/update-password', methods=['PUT'])
@auth_token
def update_password_api(email): return update_password(email)


@app.route('/uploads/<folder>/<filename>', methods=['GET'])
def get_uploaded_file(filename, folder):
    return send_from_directory('public/'+folder+'/', filename)


@app.route('/classify', methods=['POST'])
@auth_token
def classify_api(email): return classify_image(email)


@app.route('/chat', methods=['POST'])
@auth_token
def chat_bot_api(email): return chatBot_controller()


if __name__ == '__main__':
    app.run(host=os.getenv('HOST')
            or 'localhost', port=os.getenv('PORT') or 3000)
