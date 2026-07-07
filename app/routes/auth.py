from flask import Blueprint
from app.handlers.auth_handler import login, logout, fetchData
from app.handlers.users_handler import fetchAllUser, fetchHRISUsers, addMFAUSer, resetKey, resetPass, UpdateUserData

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/login", methods=["POST"])(login)
auth_bp.route("/logout", methods=["POST"])(logout)
auth_bp.route("/user/<userId>", methods=["GET"])(fetchData)
auth_bp.route("/user", methods=["GET"])(fetchAllUser)
auth_bp.route("/usersFromHRIS", methods=["GET"])(fetchHRISUsers)
auth_bp.route("/userCreation", methods=["POST"])(addMFAUSer)
auth_bp.route("/userResetKey/<Id>", methods=["PUT"])(resetKey)
auth_bp.route("/userResetPass/<Id>", methods=["PUT"])(resetPass)
auth_bp.route("/userUpdateData/<Id>", methods=["PUT"])(UpdateUserData)