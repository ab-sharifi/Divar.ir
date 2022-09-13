from flask import render_template


def check_email(email):
    import re
    # regex for email validation
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+') 
    if re.fullmatch(regex, email):
        return True
    return False