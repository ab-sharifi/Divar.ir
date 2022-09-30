"""
    This Script added cities to DB automatically and
    refrenced to each State in db
    DB data comes from ==> : https://github.com/ahmadazizi/iran-cities.git
"""
import os
import csv
from divar import db
from divar.models import City, State
from views.helpers import persian


"""
schema of csv headers: 
        id, name ,shahr_type ,ostan ,shahrestan ,bakhsh
"""

def add_city():
    with open(os.path.join("./views/csv/shahrestan.csv"), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)   
        for city in reader:
            name , state_id = city["name"], city["ostan"]    
            
            # find state first
            state_db = State.query.filter(State.id == int(state_id)).first()    
            if not state_db:
                print(f"Not found {name}")
                continue

            new_city = City(city_name=name,state_Cities=state_db)
            try:
                db.session.add(new_city)
                db.session.commit()
                print(persian(name),persian(" اضافه شد "))
            except:
                db.session.rollback()
                continue