from flask import request, jsonify
from models.user import create_connection, create_user_table, hash_password, register_user, get_user_by_email, verify_password
from helpers.jwt_helper import generate_jwt


def register(app):
    '''Function to handel user registration request'''
    fullName = request.form.get('fullName')
    email = request.form.get('email')
    password = request.form.get('password')
    city = request.form.get('city')
    phoneNumber = request.form.get('phoneNumber')

    if get_user_by_email(email):
        return jsonify({'status': False, 'message': "User already exists", 'data': None}), 400

    hashed_password = hash_password(password)
    register_user(email, hashed_password, fullName,
                  city, phoneNumber)

    token = generate_jwt(email, app)
    return jsonify({'status': True, 'message': "User created successfully", 'data': {'fullName': fullName, 'email': email, 'city': city, 'phoneNumber': phoneNumber, 'token': token}})


def login(app):
    '''Function to handel user login request'''
    data = dict(request.form)
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"status": False, 'message': 'Email and password are required!', 'data': None}), 400
    email = data["email"]
    password = data["password"]
    user = get_user_by_email(email)
    if not user:
        return jsonify({"status": False, 'message': 'User not found', 'data': None}), 404
    if not verify_password(user[3], password):
        return jsonify({"status": False, 'message': 'Invalid password', 'data': None}), 401
    token = generate_jwt(data["email"], app)

    return jsonify({'status': True, 'message': "User login successfully", 'data': {'fullName': user[1], 'email': user[2], 'city': user[4], 'phoneNumber': user[5], 'token': token}}), 200


def get_user_data(email):
    '''Function to get user data'''
    user = get_user_by_email(email)
    if not user:
        return jsonify({'status': False, 'message': 'User not found', 'data': None}), 404
    return jsonify({'status': True, 'message': 'User data fetched successfully', 'data': {'fullName': user[1], 'email': user[2], 'city': user[4], 'phoneNumber': user[5]}})


def update_user_data(email):
    user = get_user_by_email(email)
    inputData = [user[1], user[4], user[5]]
    if not user:
        return jsonify({'status': False, 'message': 'User not found', 'data': None}), 404
    data = request.get_json()
    if 'fullName' in data:
        inputData[0] = data['fullName']
    if 'city' in data:
        inputData[1] = data['city']
    if 'phoneNumber' in data:
        inputData[2] = data['phoneNumber']
    conn = create_connection()
    create_user_table(conn)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET fullName = ?, city = ?, phoneNumber = ? WHERE email = ?",
                   (inputData[0], inputData[1], inputData[2], email))
    conn.commit()
    cursor.close()
    conn.close()
    user = get_user_by_email(email)
    return jsonify({'status': True, 'message': 'User data updated successfully', 'data': {'fullName': user[1], 'email': user[2], 'city': user[4], 'phoneNumber': user[5]}})


def update_password(email):
    user = get_user_by_email(email)
    if not user:
        return jsonify({'status': False, 'message': 'User not found', 'data': None}), 404
    data = request.get_json()
    old_password = data['old_password']
    if not verify_password(user[3], old_password):
        return jsonify({'status': False, 'message': 'Worng old password', 'data': None}), 401
    new_password = data['new_password']
    hashed_password = hash_password(new_password)
    conn = create_connection()
    create_user_table(conn)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE email = ?",
                   (hashed_password, email))
    conn.commit()
    cursor.close()
    conn.close()
    user = get_user_by_email(email)
    return jsonify({'status': True, 'message': 'Password updated successfully'})
