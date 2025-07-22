from models.Category import Category
from database import db

class CategoryRepository:

    # GETTERS
    @staticmethod
    def get_all():
        return Category.query.order_by(Category.order).all()

    @staticmethod
    def get_by_sex(sex):
        return Category.query.filter_by(sex=sex).order_by(Category.order).all()

    #INSERT
    @staticmethod
    def insert_categories(categories):
        db.session.add_all(categories)
        db.session.commit()

    # DELETE
    @staticmethod
    def delete_all():
        Category.query.delete()
        db.session.commit()
