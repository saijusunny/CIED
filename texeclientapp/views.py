from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import datetime,date, timedelta
import pywhatkit
from django.core.mail import send_mail
import random
import string
from django.conf import settings
from django.http import JsonResponse
def index(request):
    return render(request, 'index.html',{'user':None})

def login_main(request):
    if request.method == 'POST':
        username  = request.POST['username']
        password = request.POST['password']
   
        user = authenticate(username=username, password=password)
        try:
    
            if User_Registration.objects.filter(username=request.POST['username'], password=request.POST['password'],role="user1").exists():

                member = User_Registration.objects.get(username=request.POST['username'],password=request.POST['password'])
                
                request.session['userid'] = member.id
                
                return redirect('staff_home')
                        
            
                
                
            elif User_Registration.objects.filter(username=request.POST['username'], password=request.POST['password'],role="user2").exists():
                member = User_Registration.objects.get(username=request.POST['username'],password=request.POST['password'])
                request.session['userid'] = member.id
                if member.status=="deactive":
                    messages.error(request, 'Account Deactivated From Admin')
                else:
                    return redirect('home')
            

            elif user.is_superuser:
                    request.session['userid'] = request.user.id
                    return redirect('admin_home')
            else:
                messages.error(request, 'Invalid username or password')
        except:
            messages.error(request, 'Invalid username or password')
    

    return render(request,'login.html')

def logout(request):
    if 'userid' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')


#############################################################Admin Module
def admin_home(request): 
    return render(request, 'admin/admin_home.html',)

def admin_add_item(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        title = form_data.get('title', None)
        price = form_data.get('price', None)
        offer_percentage = form_data.get('offer_percentage', None)
        offer_prices = form_data.get('offer_price', None)
        image = request.FILES.get('image', None)
        category_id = form_data.get('categories', None)
        under_category = form_data.get('under_category', None)
        title_description = form_data.get('title_description', None)
        description = form_data.get('description', None)
        sub_categoryies = form_data.get('subcategories', None)
       
        new_item = item(
            name = title,
            price = price,
            offer = offer_percentage,
            offer_price=offer_prices,
            image = image,
            title_description = title_description,
            description = description
        )
        new_item.save()
        return redirect('admin_home')
   

    return render(request,'admin/ad_add_item.html')


def admin_edit_item(request, item_id):
    item_instance = get_object_or_404(item, pk=item_id)

    if request.method == 'POST':
        form_data = request.POST.dict()
        item_instance.name = form_data.get('title', '')
        item_instance.price = form_data.get('price', '')
        item_instance.offer = form_data.get('offer_percentage', '')
        item_instance.offer_price = form_data.get('offer_price', '')
        item_instance.image = request.FILES.get('image', item_instance.image)

        item_instance.title_description = form_data.get('title_description', '')
        item_instance.description = form_data.get('description', '')
        item_instance.save()
        return redirect('admin_itemlist')

    return redirect('admin_itemlist')


def admin_delete_item(request,id):
    d1=item.objects.get(id=id)
    d1.delete()
    return redirect('/admin_home/')


def admin_itemlist(request):
    items = item.objects.all()
    return render(request, 'admin/admin_itemlist.html',{'items':items})


def add_staff(request):
    if request.method == "POST":
        passwordss = request.POST.get('password',None)
        cn = request.POST.get('password',None)
        email = request.POST.get('email',None)
        username = request.POST.get('username',None)
        
        if passwordss==cn:
            if User_Registration.objects.filter(email=email).exists():
                messages.error(request,"Email already Exist")
                return redirect ("add_staff")
            else:
                if User_Registration.objects.filter(username=username).exists():
                    messages.error(request,"Username already Exist")
                    return redirect ("add_staff")
                else:
                    form=User_Registration()
                    form.name = request.POST.get('name',None)
                    form.date_of_birth = request.POST.get('date_of_birth',None)
                    form.phone_number = request.POST.get('phone_number',None)
                    form.email = request.POST.get('email',None)
                    form.username = request.POST.get('username',None)
                    digits = string.digits
                    passw = ''.join(random.choices(digits, k=6))
                    form.password=passw
                    form.addres = request.POST.get('address',None)
                    form.location= request.POST.get('location')
                   
                    form.pro_pic=request.FILES.get('pics',None)
                    form.role="user1"
                    form.access= request.POST.get('access',None)
                    form.save()

                    subject = "CIED ACCOUNT DETAILS"
                    message =f'Greetings From CIED\n\n Hi {form.username},\nYour Username: {form.username},\n Your Password: {form.password},\n Thank You'

                    email_from = settings.EMAIL_HOST_USER
                    recipient_list=form.email
                    send_mail(subject,
                    message,
                    email_from,
                    [recipient_list],
                    fail_silently=True)
                #messages.success(request,"User Added Successfully")
                    return redirect ("staff_all_list")

        else:
            messages.error(request,"Username already Exist")

        return redirect ("staff_all_list")
    return render(request, "admin/admin_addstaff.html")


def staff_all_list(request):
    staff_members = User_Registration.objects.filter(role='user1')


    return render(request, 'admin/admin_stafflist.html', {'staff_members': staff_members})


def edit_staff(request,id):
 
    if request.method == "POST":
        passwordss = request.POST.get('password',None)
        cn = request.POST.get('password',None)
        email = request.POST.get('email',None)
        username = request.POST.get('username',None)
        if passwordss == None:
                form = User_Registration.objects.get(id=id)
                form.name = request.POST.get('name',None)
                form.date_of_birth = request.POST.get('date_of_birth',None)
                form.phone_number = request.POST.get('phone_number',None)
                form.email = request.POST.get('email',None)
                form.username = request.POST.get('username',None)
            
                form.addres = request.POST.get('address',None)
                form.location= request.POST.get('location')
                if request.FILES.get('pics',None)==None:
                    pass
                else:
                    form.pro_pic=request.FILES.get('pics',None)
            
                form.access= request.POST.get('access',None)
                form.save()
                return redirect ("staff_all_list")

        else:
            form = User_Registration.objects.get(id=id)

            if passwordss==cn:
              
                form.name = request.POST.get('name',None)
                form.date_of_birth = request.POST.get('date_of_birth',None)
                form.phone_number = request.POST.get('phone_number',None)
                form.email = request.POST.get('email',None)
                form.username = request.POST.get('username',None)
                
                form.password=passwordss
                form.addres = request.POST.get('address',None)
                form.location= request.POST.get('location')
            
                if request.FILES.get('pics',None)==None:
                    pass
                else:
                    form.pro_pic=request.FILES.get('pics',None)
                
                form.access= request.POST.get('access',None)
                form.save()


                
                #messages.success(request,"User Added Successfully")
                return redirect ("staff_all_list")

            else:
                messages.error(request,"Check Password")
            
                return redirect ("staff_all_list")
    return redirect ("staff_all_list")

def delete_staff(request,id):
    form = User_Registration.objects.get(id=id)
    form.delete()
    return redirect ("staff_all_list")


def ad_view_order(request):
    chk=checkout.objects.all().order_by("-id")
    chk_item=checkout_item.objects.all().order_by("-id")
    context={
        "chk":chk,
        "chk_item":chk_item,

    }
    return render(request,'admin/ad_view_order.html',context)

def user_list_view(request):
    staff_members = User_Registration.objects.filter(role='user2')
    return render(request, 'admin/user_list_view.html', {'staff_members': staff_members})
def ad_delete_check(request,id):
        chk=checkout.objects.get(id=id)
        chk_item=checkout_item.objects.filter(checkout_id=id)
        chk_item.delete()
        chk.delete()
        return redirect('ad_view_order')

def edit_user(request):
    ele = request.GET.get('ele')
    ids = request.GET.get('idss')
    us=User_Registration.objects.get(id=ids)
    us.status=ele
    us.save()
    return redirect ("user_list_view")

def delete_user(request,id):
    form = User_Registration.objects.get(id=id)

    form.delete()

    return redirect ("user_list_view")
#------------------------------------------------------- User Module
def user_regi(request):
    if request.method == "POST":
        form = User_Registration()
        passwordss = request.POST.get('password',None)
        cn = request.POST.get('password',None)
        email = request.POST.get('email',None)
        username = request.POST.get('username',None)
        if passwordss==cn:
            if User_Registration.objects.filter(email=email).exists():
                messages.error(request,"Email already Exist")
                return redirect ("user_regi")
            else:
                if User_Registration.objects.filter(username=username).exists():
                    messages.error(request,"Username already Exist")
                    return redirect ("user_regi")
                else:

                    form.name = request.POST.get('name',None)
                    form.date_of_birth = request.POST.get('date_of_birth',None)
                    form.phone_number = request.POST.get('phone_number',None)
                    form.email = request.POST.get('email',None)
                    form.username = request.POST.get('username',None)
                    form.password = request.POST.get('password',None)
                    form.addres = request.POST.get('address',None)
                    form.location= request.POST.get('location')
                    form.pro_pic=request.FILES.get('pic',None)
                    form.role="user2"
                    form.save()
                #messages.success(request,"User Added Successfully")
                    return redirect ("login_main")

        else:
            messages.error(request,"Username already Exist")
            return redirect ("user_regi")
    return render (request,"user/profile.html")

def home(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')

    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    
    crt_cnt=cart.objects.filter(user=usr).count()
    context={
            'user':usr,
            'crt_cnt':crt_cnt
         
        }
    return render (request,"user/home.html",context)
def all_item(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    

    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    items=item.objects.all()
    crt_cnt=cart.objects.filter(user=usr).count()
    context={
            'user':usr,
            "items":items,
            'crt_cnt':crt_cnt
        }
    return render (request,"user/all_items.html",context)

def all_items_add_cart(request, id):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    
    items=item.objects.get(id=id)

    if cart.objects.filter(user=usr,item=items).exists():
        messages.error(request, 'This item is already in cart')
        return redirect("all_item")
   
    else:
        crt=cart()
        crt.user=usr
        crt.item=items
        crt.save()
        messages.error(request, 'This item is add to cart')
        items=item.objects.all()
        usrd=User_Registration.objects.get(id=ids)
        context={
            'user':usrd,
            "items":items
        }
    return redirect("cart_checkout")

def product_view(request, item_id):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    crt_cnt=cart.objects.filter(user=ids).count()
    try:
        item_instance = item.objects.get(id=item_id)
        oprice = item_instance.price

        if item_instance.offer:
            off = item_instance.offer
            rp = oprice - (oprice * (off / 100))
        else:
            rp = oprice

        return render(request, 'user/productview.html', {'item': item_instance, 'rp': rp,'user':usr,"crt_cnt":crt_cnt})

    except item.DoesNotExist:
        # Handle the case where the item does not exist
        return HttpResponse("Item not found", status=404)


def cart_checkout(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    carts=cart.objects.filter(user=ids)
    crt_cnt=cart.objects.filter(user=ids).count()
  
    context={
        "cart":carts,
        'user':usr,
        "crt_cnt":crt_cnt
        
    }
    return render(request, 'user/cart.html',context)


def delete_cart(request,id):
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    ckt=cart.objects.get(user=usr,id=id).delete()
    return redirect("cart_checkout")


def send_receipt(request):
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)

    if request.method =="POST":
        total_amount = request.POST.get('total_amount')

        chk=checkout()
        chk.user = usr
        chk.profile = usr
        chk.status = "pending"
        chk.total_amount=total_amount
        chk.date=datetime.now()
        chk.save()
        item_id =request.POST.getlist('item_id[]') 
        qty =request.POST.getlist('qty[]') 

        if len(item_id)==len(qty):
            mapped2 = zip(item_id,qty)
            mapped2=list(mapped2)
         
            for ele in mapped2:
                itm=item.objects.get(id=ele[0])
               
                created = checkout_item.objects.create(item=itm,qty=ele[1],item_name=itm.name,item_price=itm.offer_price, checkout=chk)

        chk_item=checkout_item.objects.filter(checkout_id=chk)
      
        lst=""
        for i in chk_item:
            rcp="\n\nItem : "+str(i.item_name)+'\nAmount : '+str(i.item_price)+' * '+str(i.qty)+' = '+str(i.item_price)
            lst+=rcp
     
        tot="\n\nTotal Amount : "+str(total_amount)
        
        message = 'Greetings from Malieakal\n\nReciept,\n\nName :'+str(usr.name)+'\nAddress :'+str(usr.addres
        )+'\n\n'+str(lst)+str(tot)
      
        pywhatkit.sendwhatmsg_instantly(
            phone_no="+918848937577", 
            message=""+str(message),
        )
     
        messages.error(request, 'Purchase Success Full')
        
        for i in item_id:
            ckt=cart.objects.get(user=usr,item_id=i).delete()
        
          
    
        return redirect("cart_checkout")
    return redirect("cart_checkout")


def staff_home(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    context={
   
        'user':usr,
   
        
    }
    return render(request, 'staff/staff_home.html',context)

def staff_view_order(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    chk=checkout.objects.all().order_by("-id")
    chk_item=checkout_item.objects.all().order_by("-id")
    context={
        "chk":chk,
        "chk_item":chk_item,
        'user':usr,

    }
    return render(request,'staff/staff_view_order.html',context)

def staff_delete_check(request,id):
        chk=checkout.objects.get(id=id)
        chk_item=checkout_item.objects.filter(checkout_id=id)
        chk_item.delete()
        chk.delete()
        return redirect('staff_view_order')

def staffchange_status(request):
    ele = request.GET.get('ele')
    ids = request.GET.get('idss')
    print(ele)
    if ele == "complete":
        digits = string.digits
        otp = ''.join(random.choices(digits, k=6))
        ser=checkout.objects.get(id=ids)
        ser.otp=otp
        mail=ser.user.email
        ser.save()

        subject = "Greetings From CIED"
        message =f'Hi {mail},\nYour Email Order Verification OTP is: {otp}'

        email_from = settings.EMAIL_HOST_USER
        recipient_list=mail
        send_mail(subject,
        message,
        email_from,
        [recipient_list],
        fail_silently=True)
        print("haii")
        pass
    else:
        pass

    return JsonResponse({"status":" not"})

def chk_otp(request,id):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    if request.method == "POST":
        ser=checkout.objects.get(id=id)
        otp=request.POST.get('quesry', None)
        if int(otp) == int(ser.otp):
            ser.status="complete"
            ser.delivery_date=date.today()
            ser.staff=ids
            ser.save()
            return redirect('staff_view_order')
        else:
            return redirect('staff_view_order')
    else:
       return redirect('staff_view_order') 
  