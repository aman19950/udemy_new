from django.contrib import admin

# Register your models here.
from . models import *

class all_learning(admin.TabularInline):
    model = learning 

class all_pre_req(admin.TabularInline):
    model = pre_req 

class all_video_info(admin.ModelAdmin):
    inlines = [all_learning,all_pre_req]

admin.site.register(user_signup)
admin.site.register(course_dtls,all_video_info)
admin.site.register(video)
admin.site.register(UserCourse)
admin.site.register(payment)
admin.site.register(Refcode)
