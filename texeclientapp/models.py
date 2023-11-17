from django.db import models
role = (
    ("user1", "Staff"),
    ("user2", "User"),
   
)
# Create your models here.
class User_Registration(models.Model):
    
    name = models.CharField(max_length=255,blank=True,null=True)
    phone_number = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    role = models.CharField(max_length=255,blank=True,null=True,choices = role)
    pro_pic = models.ImageField(upload_to='images/propic', default='static/images/logo/icon.png')
    username = models.CharField(max_length=255,blank=True,null=True)
    password = models.CharField(max_length=255,blank=True,null=True)
    status =models.CharField(max_length = 255,blank=True,null=True, default="active")
    addres =  models.TextField(blank=True,null=True)
    joindate = models.DateField(null=True)
    date_of_birth = models.DateField(null=True)
    last_login = models.DateTimeField(null=True, blank=True)    
    location= models.CharField(max_length=255,blank=True,null=True)
    def str(self):
        return self.nickname
    
    def get_email_field_name(self):
        return 'email'

class item(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255,blank=True,null=True)
    title_description = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=255,blank=True,null=True)
    price = models.FloatField(default=0)
    offer_price=  models.FloatField(default=0)
    offer = models.IntegerField(default=0)
    image = models.FileField(upload_to='images/items', default='static/images/logo/noimage.jpg')
   


class cart(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(item, on_delete=models.SET_NULL, null=True, blank=True)

class checkout(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount=models.FloatField(default=0,null=True, blank=True)
    date=models.DateTimeField(null=True, blank=True)



class checkout_item(models.Model):
    checkout = models.ForeignKey(checkout, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(item, on_delete=models.SET_NULL, null=True, blank=True)
    item_name= models.CharField(max_length=255,blank=True,null=True)
    qty=models.IntegerField(null=True, blank=True)
    item_price=models.FloatField(null=True, blank=True)


