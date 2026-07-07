from flask import jsonify, request, session, make_response
from app.models.user import User
from app.services.auth_services import hash_password
from sqlalchemy import and_, null
from database import db
import urllib.parse

def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    hash_pass = hash_password(password)


    user = User.query.filter(
        and_(
            User.EmployeeId == username,
            User.Password == hash_pass
            )
    ).first()
    if user:
        return jsonify({"message": "Login successful", "status": "success", "user" : username}), 200
    else:
        return jsonify({"message": "Invalid credentials", "status": "error"}), 401
    

def fetchData(userId):

    user = User.query.filter_by(EmployeeId = userId).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())  # Assuming to_dict() exists

def logout():

    session.clear()
    response = make_response(jsonify({"message": "Logged out successful!"}), 200)

    response.set_cookie('session', '', expires=0)
    return response

    
