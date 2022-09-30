"""
This Script added all State in Iran To db automatically
DB data comes from ==> : https://github.com/ahmadazizi/iran-cities.git
"""

import csv
import os
from divar.models import State
from divar import db
from views.helpers import persian


def add_state():
    with open(os.path.join("./views/csv/ostan.csv"), "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for (id,state) in reader:
            # skip first row
            if state == "name":
                continue
            new_state = State(state_name=state)
            try:
                db.session.add(new_state)
                db.session.commit()
                print(persian("اضافه شد"), persian(state), persian("استان") )
            except:
                db.session.rollback()
                continue