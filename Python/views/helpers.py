import re
import random
from divar.models import MailVerification

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




    
