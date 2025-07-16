from repositories.CategoryRepository import CategoryRepository
from models.Category import Category

category_repository = CategoryRepository()

def init_categories():
    category_repository.delete_all()
    categories = []
    categories.append(Category("Jeune M", "J", "M", 1))
    categories.append(Category("Senior M", "S", "M", 2))
    categories.append(Category("35+ M", "35+", "M", 3))
    categories.append(Category("45+ M", "45+", "M", 4))
    categories.append(Category("55+ M", "55+", "M", 5))
    categories.append(Category("65+ M", "65+", "M", 6))
    categories.append(Category("Jeune F", "J", "F", 1))
    categories.append(Category("Senior F", "S", "F", 2))
    categories.append(Category("35+ F", "35+", "F", 3))
    categories.append(Category("45+ F", "45+", "F", 4))
    categories.append(Category("55+ F", "55+", "F", 5))
    category_repository.insert_categories(categories)