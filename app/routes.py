from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from .routes_helpers import validate_model

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# GET ALL ENDPOINT
@bp.route("", methods=["GET"])
def handle_tasks():
    title_param = request.args.get("title")
    if title_param:
        tasks = Task.query.filter_by(title=title_param)
    else:
        tasks = Task.query.all()
    tasks_list = [task.to_dict() for task in tasks]

    return jsonify(tasks_list), 200


# CREATE ENDPOINT
@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(f"task {new_task.title} successfully created", 201)


# GET ONE ENDPOINT
@bp.route("/<id>", methods=["GET"])
def handle_task(id):
    task = validate_model(Task, id)
    result=dict(task=task.to_dict())
    return make_response(jsonify(result),200)

# UPDATE ONE ENDPOINT
@bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()

    return make_response(f"task {task.title} successfully updated", 200)


# DELETE ONE ENDPOINT
@bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"task {task.title} successfully deleted", 200)

