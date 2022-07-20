from django.db import models
from torch import mode


# Create your models here.


class user_signup(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    mobile = models.BigIntegerField()
    gender = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name


class course_dtls(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False)
    desc = models.CharField(max_length=200)

    image = models.ImageField(upload_to='image/')

    def __str__(self):
        return self.name


class video(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    s_no = models.IntegerField()
    course_name = models.ForeignKey(course_dtls, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=200)
    is_preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserCourse(models.Model):
    user_name = models.ForeignKey(user_signup, on_delete=models.CASCADE)
    course_name = models.ForeignKey(course_dtls, on_delete=models.CASCADE)
    # date =

    def __str__(self):
        return self.user_name.first_name


class payment(models.Model):
    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=200)
    user = models.ForeignKey(user_signup, on_delete=models.CASCADE)
    course = models.ForeignKey(course_dtls, on_delete=models.CASCADE)
    user_course = models.ForeignKey(
        UserCourse, null=True, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.order_id

class Refcode(models.Model):
    code = models.CharField(max_length=100)
    user_course = models.ForeignKey(course_dtls,on_delete=models.CASCADE)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.code



class course_info(models.Model):
    desc =  models.CharField(max_length=500)
    course = models.ForeignKey(course_dtls,on_delete=models.CASCADE)

    class Meta:
        abstract = True
        
class learning(course_info):
    pass


class pre_req(course_info):
    pass

# class learning(course_info):
#     pass