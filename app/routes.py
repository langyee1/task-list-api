from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from .routes_helpers import validate_model

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# GET ALL ENDPOINT
@bp.route("", methods=["GET"])
def handle_cats():
    pass

