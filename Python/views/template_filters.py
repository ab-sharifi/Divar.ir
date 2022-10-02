import os
from divar import app


@app.template_filter("path")
def path(v):
    
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
        return (os.path.join("static/uploads" , "posts" , v))
    else:
        return (os.path.join("static/uploads" , "posts" , images[0]))

