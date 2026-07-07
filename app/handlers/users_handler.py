from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from sqlalchemy import null, and_
from database import db
from app.models.hrisEmployees import HRISEmployees
from app.services.auth_services import hash_password
import time

def fetchAllUser():
    users = User.query.all()
    if not users:
        return jsonify({"error": "Error fetching users"}), 401
    return jsonify([user.to_dict() for user in users])

def fetchHRISUsers():
    hris_users = HRISEmployees.query.filter_by(Tag='Active').order_by(HRISEmployees.FullName).all()
    if not hris_users:
        return jsonify({"error": "Error fetching HRIS users"}), 401
    return jsonify([hris_user.to_dict() for hris_user in hris_users])

def addMFAUSer():
    try:
        data = request.get_json()
        status = 1

        checkExisting = User.query.filter(
            and_(
                User.EmployeeId==data["EmployeeId"],
                User.OASId==data["MFAID"]
            )
        ).first()
        if checkExisting:
            return jsonify({
                "error": "User already exists!",
                "details": "Employee ID or MFA ID already in use."
            }), 409

        newUser = User(
            OASId=data["MFAID"],
            EmployeeId=data["EmployeeId"],
            EmployeeName=data["FullName"],
            EmailAddress=data["EmailAddress"],
            Status=status
        )
        db.session.add(newUser)
        db.session.commit()

        return jsonify({"message" : "User created successfully!"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e.orig)}), 400
    except Exception as e:
        return jsonify({"error": "Something went wrong", "details" : str(e)}, 500)
    
def resetKey(Id):
    resetUser = User.query.filter(User.OASId==Id).first()
    if not resetUser:
        return jsonify({"error": "User not found."}), 404
    
    resetUser.SecretKey = None
    db.session.commit()
    return jsonify({"message" : "Secret key has been successfully reset!"}), 200


def resetPass(Id):
    resetPass = User.query.filter(User.OASId==Id).first()
    if not resetPass:
        return jsonify({"error": "User not found."}), 404
    
    employeeid = resetPass.EmployeeId
    setPass = f"KWE{employeeid}"
    hashedPass = hash_password(setPass)


    resetPass.Password = hashedPass
    db.session.commit()
    return jsonify({"message" : "Password has been successfully reset!"}), 200

def UpdateUserData(Id):
    data = request.get_json()

    user = User.query.filter(User.OASId==Id).first()
    if not user:
        return jsonify({"message" : "User not found."})
    
    if 'EmployeeName' in data:
        user.EmployeeName = data['EmployeeName']
    if 'EmailAddress' in data:
        user.EmailAddress = data['EmailAddress']
    if 'Status' in data:
        user.Status = data['Status']

    try:
        db.session.commit()
        return jsonify({"message": "User profile has been successfully updated!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update user", "details": str(e)}), 500
    