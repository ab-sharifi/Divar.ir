import os
from divar import app


@app.template_filter("path_index")
def path_index(v):
    """
    This filter take a value and return a path url to static in server
    used in index home for little post picture path
    """
    if "[" in v:
        v = v.replace("[","")
    
    if "]" in v:
        v = v.replace("]","")
        
    if "'" in v:
        v = v.replace("'","")
    
    if "'" in v:
        v = v.replace("'","")

    images = v.split(",")
    
    if len(images) == 0:
        return (os.path.join("/static/uploads" , "posts" , v))
    else:
        return (os.path.join("/static/uploads" , "posts" , images[0]))



@app.template_filter("url_post")
def url_post(v):
    """
    This filter take a value and return it to a url_path
    used for index home urls ==> divar.ir/v/ماشین-سالم
    """
    temp = v.split(" ")
    value = "" 
    for x in temp:
        value += "-" + x
    # remove first - and return
    return( value.replace("-", "", 1) )


@app.template_filter("path_images")
def path_images(v):
    """
    this filter take a value and return path to that file(value) in static in server
    used in post pages for slider image
    """
    if "[" in v:
        v = v.replace("[","")
    
    if "]" in v:
        v = v.replace("]","")
        
    if "'" in v:
        v = v.replace("'","")
    
    if "'" in v:
        v = v.replace("'","")
    
    v = v.split(",")
    
    value = [] 

    for each in v:
        value.append(str(os.path.join("/static/uploads","posts",each.strip())))
    
    return value




from divar.models import Category
from views import helpers
@app.template_filter("get_categories")
def get_categories(v):
    """
    This filter take a string list of categories id and return value of categories
    used in post page for display tag of categories  
    """
    
    if "[" in v:
        v = v.replace("[","")
    
    if "]" in v:
        v = v.replace("]","")
        
    if "'" in v:
        v = v.replace("'","")
    
    if "'" in v:
        v = v.replace("'","")
    
    v= v.split(",")
    values = []

    for each in v:
        try:
            each = int(each)
        except ValueError:
            continue
        res = Category.query.filter(Category.id == each).first()
        if res:
            values.append(res.category)

    return values 


from divar.models import User
@app.template_filter("get_email")
def get_email(v):
    """
    This filter take an user id and return email of it
    used in post page show information btn
    """
    try:
        v= int(v)
    except ValueError:
        return "None"
    temp = User.query.filter (User.id == v).first()
    if temp :
        return temp.email
    return "None" 