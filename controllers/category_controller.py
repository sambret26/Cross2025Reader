
from flask import Blueprint, jsonify
from repositories.CategoryRepository import CategoryRepository

category_repository = CategoryRepository()

category_bp = Blueprint("category_controller", __name__, url_prefix="/categories")

@category_bp.route("/", methods=["GET"])
def get_categories():
    categories = category_repository.get_all()
    return jsonify([category.to_json() for category in categories])