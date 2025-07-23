from repositories.CategoryRepository import CategoryRepository
from models.Category import Category

category_repository = CategoryRepository()

def init_categories():
    category_repository.delete_all()
    categories = []
    # Scratch
    categories.append(Category("Scratch M", True, "1", "M", 1))
    categories.append(Category("Scratch F", True, "1", "F", 1))
    categories.append(Category("Scratch M", True, "2", "M", 2))
    categories.append(Category("Scratch F", True, "2", "F", 2))
    categories.append(Category("Scratch M", True, "3", "M", 3))
    categories.append(Category("Scratch F", True, "3", "F", 3))
    categories.append(Category("Scratch M", True, "4", "M", 4))
    categories.append(Category("Scratch M", True, "5", "M", 5))

    # Categories
    categories.append(Category("Jeune M", False, "J", "M", 1))
    categories.append(Category("Senior M", False, "S", "M", 2))
    categories.append(Category("35+ M", False, "35+", "M", 3))
    categories.append(Category("45+ M", False, "45+", "M", 4))
    categories.append(Category("55+ M", False, "55+", "M", 5))
    categories.append(Category("65+ M", False, "65+", "M", 6))
    categories.append(Category("Jeune F", False, "J", "F", 1))
    categories.append(Category("Senior F", False, "S", "F", 2))
    categories.append(Category("35+ F", False, "35+", "F", 3))
    categories.append(Category("45+ F", False, "45+", "F", 4))
    categories.append(Category("55+ F", False, "55+", "F", 5))

    # Oriol
    categories.append(Category("Oriol M", False, "O", "M", 7))
    categories.append(Category("Oriol F", False, "O", "F", 7))

    category_repository.insert_categories(categories)