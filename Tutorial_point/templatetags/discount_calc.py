
from tkinter.messagebox import NO
from django import template
from ..models import *

register = template.Library()


@register.simple_tag
def price_discount(price, discount):
    print(price, discount)
    if discount is None or discount == 0:
        return price
    else:
        s = int(price * ((100-discount) * 0.01))
        return s


@register.simple_tag
def is_enroll(request,course):

    user  = None
    try:
        if not request.session['name']:
            return False
    except:
        return False
    user = user_signup.objects.get(first_name = request.session['name'])

    try:
        user = UserCourse.objects.get(user_name = user , course_name = course)
        print("i am here")
        return True
    except:
        return False
    

