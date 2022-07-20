from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="home"),
    path("contact", views.contact_dtls, name="con"),
    path("registration", views.sign_up, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path('course/<str:slug>', views.course_information, name="course"),
    # path('course', views.course_information, name="cou"),
    path('checkout/<str:slug>', views.checkout, name="checkout"),
    path('verify_payment', views.verify_payment, name="verifypayment"),



]
