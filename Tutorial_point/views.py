from django.http import HttpResponse
from django.shortcuts import redirect, render
from time import time

from sympy import re

from . models import *
# Create your views here.
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
import razorpay
from udemy.settings import *
client = razorpay.Client(auth=(key_id, secret_id))


def index(request):

    course_info = course_dtls.objects.all()

    return render(request, 'home.html', {'course_info': course_info})


def contact_dtls(request):
    return render(request, 'contact.html')


def sign_up(request):
    if request.method == "POST":
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')

        save_info = user_signup(first_name=fname, last_name=lname, email=email,
                                password=make_password(password), mobile=mobile, gender=gender)
        save_info.save()

        return HttpResponse("registration succsessfull")


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            fetch_info = user_signup.objects.get(email=email)
            if(check_password(password, fetch_info.password)):

                # print("you have entered correct password")
                request.session['name'] = fetch_info.first_name
                request.session['email'] = fetch_info.email
                return redirect('home')

            else:
                return HttpResponse("please enter a valid password")

        except:
            return HttpResponse("please enter a valid email....")


def logout(request):

    request.session.clear()
    return redirect('home')


def course_information(request, slug):

    fetch_dtls = course_dtls.objects.get(slug=slug)
    s_no = request.GET.get('serial_no')
    videos = None
    if s_no is None:
        s_no = 1
    try:
        videos = video.objects.get(course_name=fetch_dtls, s_no=s_no)
        if videos.is_preview is False:
            if request.session.get('name') is None:
                return redirect('home')
            else:
                user_id = user_signup.objects.get(
                    email=request.session['email'])
                try:
                    user_course = UserCourse.objects.get(
                        user_name=user_id, course_name=fetch_dtls)
                    print(user_course)
                except:
                    return redirect('checkout', slug=fetch_dtls.slug)
    except:
        return redirect('home')

    return render(request, 'course_dtls.html', {'co_dtls': fetch_dtls, 'video': videos})


def checkout(request, slug):
    course = course_dtls.objects.get(slug=slug)
    user_id = user_signup.objects.get(email=request.session['email'])
    action = request.GET.get('action')
    coup = request.GET.get('coupon')

    error = None
    cpn_code_msg = None
    amount = None

    order_ids = None
    notes = None
    cpn_code = None
    if error is None:
        amount = int(course.price * ((100-course.discount) * 0.01)*100)

    if coup:
        try:
            cpn_code = Refcode.objects.get(course=course,code=coup)
            amount = int(course.price * ((100-cpn_code.discount) * 0.01)*100)
        except:
            cpn_code_msg = "invalid coupon code"

    if action == 'create_payment':

        currency = "INR"
        receipt = f'Tutorial_point-{int(time())}'
        notes = {
            'user': user_id.first_name,
            'email': user_id.email
        }
        data = {
            "amount": amount,
            "currency": currency,
            "receipt": receipt,
            "notes": notes
        }
        orders = client.order.create(data=data)
        # print(payment)
        order_ids = orders.get('id')
        payments = payment()
        payments.order_id = order_ids

        payments.user = user_id
        payments.course = course
        payments.save()
    if coup == "":
        cpn_code_msg = "please enter a coupon code"
    context = {
        'user_id': user_id,
        'course': course,
        'order_id': order_ids,
        'notes': notes,
        'cpn_code_msg': cpn_code_msg,
        'coup': cpn_code,
        'error': error


    }

    return render(request, 'checkout.html', context=context)


@csrf_exempt
def verify_payment(request):
    data = request.POST
    user_id = user_signup.objects.get(email=request.session['email'])

    payment_id = data['razorpay_payment_id']
    razor_order_id = data['razorpay_order_id']
    payments = payment.objects.get(order_id=razor_order_id)
    payments.payment_id = payment_id
    payments.status = True
    user_courses = UserCourse(
        user_name=payments.user, course_name=payments.course)
    user_courses.save()
    payments.user_course = user_courses
    payments.save()

    try:
        return redirect('home')
    except:
        return HttpResponse("successfull")
