"""
    This Script added Categories to Database automatically
"""
from divar import db
from divar.models import Category
from views.helpers import categories
from views.helpers import persian

def add_category():
    for k,v in categories.items():
        new_category = Category()
        category_value = v.strip()
        new_category.category = category_value
        try:
            db.session.add(new_category)
            db.session.commit()
            print(persian(category_value), persian("اضافه شد"))
        except:
            db.session.rollback()
            continue