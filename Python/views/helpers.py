import re
import random
from divar.models import MailVerification
from flask import render_template, flash

#    TODO:
#        add to db and remove hard coded
categories = {
"category-car":"خودرو","category-home" : "خانه",
"category-digital-products":"کالای دیجیتال", "category-fun-hobby":"سرگرمی و فراغت" ,"category-services":"خذمات",
"category-sell-center":"نمایندگی فروش", "category-persoanl":"وسایل شخصی", "category-equipment":"تجهیزات و صنعتی",
"category-hire-work":"استخدام و کاریابی", "category-social":"اجتماعی", "category-unknown":"متفرقه"
}


from divar.models import Category
def check_category(category):
    """
    Check the input category and validate it
    and return id of categories if there is no category return False
    """

    id_list = []
    # check categories and return id number of each categoies in list
    for value in category:
        print(value)
        db_query = Category.query.filter(Category.category == value).first()
        if not db_query:
            continue
        else:
            id_list.append(db_query.id)

    if len(id_list) == 0:
        return False
    else:
        return id_list




def check_email(email):
    # regex for email validation
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+') 
    if re.fullmatch(regex, email):
        return True
    return False


def code_generator():
    while True:
        ver_code = random.randint(999_99,1000_000)
        # check code is not duplicate in db
        code_check_db = MailVerification.query.filter(MailVerification.active_code == ver_code).first()  
        if not code_check_db:
            break
        else:
            continue
    return ver_code

from flask import redirect, session, url_for
from functools import wraps

def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('user_id',None):
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return inner