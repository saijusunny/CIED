from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import datetime,date, timedelta

def index(request):
    return render(request, 'index.html')

def login_main(request):
    if request.method == 'POST':
        username  = request.POST['username']
        password = request.POST['password']
        print(username)
        user = authenticate(username=username, password=password)
    
    
        if User_Registration.objects.filter(username=request.POST['username'], password=request.POST['password'],role="user1").exists():

            member = User_Registration.objects.get(username=request.POST['username'],password=request.POST['password'])
            
            request.session['userid'] = member.id
            if Profile_User.objects.filter(user_id=member.id).exists():
                prop=Profile_User.objects.get(user_id=member.id)
                if prop.firstname == None:
                    return redirect('profile_staff_creation')
                else:
                    return redirect('staff_home')
                    
            else:
                return redirect('profile_staff_creation')
            
            
        elif User_Registration.objects.filter(username=request.POST['username'], password=request.POST['password'],role="user2", status="active").exists():
            member = User_Registration.objects.get(username=request.POST['username'],password=request.POST['password'])
            request.session['userid'] = member.id
            if Profile_User.objects.filter(user_id=member.id).exists():
                return redirect('home')
            else:
                return redirect('profile_user_creation')

        elif user.is_superuser:
                request.session['userid'] = request.user.id
                return redirect('admin_home')
        else:
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
        username = request.POST.get('username',None)
        email = request.POST.get('',None)
        if User_Registration.objects.filter(email=email).exists():
            messages.error(request,"Email already Exist")
            return redirect ("add_staff")
        else:
            if User_Registration.objects.filter(username=username).exists():
                messages.error(request,"Username already Exist")
                return redirect ("add_staff")
            else:
                form = User_Registration()

                form.name = request.POST.get('name',None)
                form.date_of_birth = request.POST.get('date_of_birth',None)
                form.phone_number = request.POST.get('phone_number',None)
                form.email = request.POST.get('email',None)
                form.role = "user1"
                form.username = request.POST.get('username',None)
                form.password = request.POST.get('password',None)
                form.location= request.POST.get('location')
                form.joindate=date.today()
                form.save()

        return redirect ("staff_all_list")
    return render(request, "admin/admin_addstaff.html")


def staff_all_list(request):
    staff_members = User_Registration.objects.filter(role='user1')


    return render(request, 'admin/admin_stafflist.html', {'staff_members': staff_members})


def edit_staff(request,id):

    if request.method == "POST":
        form = User_Registration.objects.get(id=id)

        form.name = request.POST.get('name',None)
        form.date_of_birth = request.POST.get('date_of_birth',None)
        form.phone_number = request.POST.get('phone_number',None)
        form.email = request.POST.get('email',None)
        form.username = request.POST.get('username',None)
        form.password = request.POST.get('password',None)
        form.location= request.POST.get('location')
        form.save()
        
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

def ad_delete_check(request,id):
        chk=checkout.objects.get(id=id)
        chk_item=checkout_item.objects.filter(checkout_id=id)
        chk_item.delete()
        chk.delete()
        return redirect('ad_view_order')


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
                    form.address = request.POST.get('address',None)
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