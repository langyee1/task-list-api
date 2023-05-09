from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import text
from app.models.task import Task
from app import db
from .routes_helpers import validate_model
from datetime import datetime

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# GET ALL ENDPOINT
@bp.route("", methods=["GET"])
def handle_tasks():

    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(text("title asc"))
    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(text("title desc"))

    else:
        tasks = Task.query.all()
    tasks_list = [task.to_dict() for task in tasks]

    return jsonify(tasks_list), 200


# CREATE ENDPOINT
@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if request_body.get("title") is None or request_body.get("description") is None:
        result=dict(details='Invalid data') 
        return make_response(jsonify(result),400)

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()
    result=dict(task=new_task.to_dict()) 
    return make_response(jsonify(result),201)


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

    db.session.commit()
    result=dict(task=task.to_dict()) 
    return make_response(jsonify(result),200)


# DELETE ONE ENDPOINT
@bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)
    result=dict(details=f'Task {task.id} "{task.title}" successfully deleted') 
    db.session.delete(task)
    db.session.commit()
    
    return make_response(jsonify(result),200)

# PATCH ONE ENDPOINT
@bp.route("/<id>/mark_complete", methods=["PATCH"])
def patch_task_complete(id):
    task = validate_model(Task, id)

    task.completed_at = datetime.now()


    db.session.commit()
    result=dict(task=task.to_dict()) 
    return make_response(jsonify(result),200)

@bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def patch_task_incomplete(id):
    task = validate_model(Task, id)

    task.completed_at = None


    db.session.commit()
    result=dict(task=task.to_dict()) 
    return make_response(jsonify(result),200)