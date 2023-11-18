from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login_main',views.login_main, name='login_main'),
    path('logout/', views.logout,name='logout'),

    #-----------------------------------------------------------admin
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_delete_item/<int:id>/', views.admin_delete_item, name='admin_delete_item'),

    path('admin_add_item',views.admin_add_item,name='admin_add_item'),
    path('admin_edit_item/<int:item_id>',views.admin_edit_item,name='admin_edit_item'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('admin_itemlist/',views.admin_itemlist,name='admin_itemlist'),
    path('staff_all_list/', views.staff_all_list, name='staff_all_list'),
    path('edit_staff/<int:id>', views.edit_staff, name='edit_staff'),
    path('delete_staff/<int:id>', views.delete_staff, name='delete_staff'),
    path('ad_view_order/', views.ad_view_order, name='ad_view_order'),
    path('ad_delete_check/<int:id>', views.ad_delete_check, name='ad_delete_check'),
    path('user_list_view/', views.user_list_view, name='user_list_view'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    #--------------------------------------------------------User Module
    path('user_regi/', views.user_regi, name='user_regi'),
    path('all_item/', views.all_item, name='all_item'),
    path('home/', views.home, name='home'),
    path('all_items_add_cart/<int:id>', views.all_items_add_cart, name='all_items_add_cart'),
    path('product_view/<int:item_id>', views.product_view, name='product_view'),
    path('cart_checkout/', views.cart_checkout, name='cart_checkout'),
    path('send_receipt/', views.send_receipt, name='send_receipt'),
    path('delete_cart/<int:id>', views.delete_cart, name='delete_cart'),
    #--------------------------------------------------------------------staff Module
    path('staff_home/', views.staff_home, name='staff_home'),
    path('staff_view_order/', views.staff_view_order, name='staff_view_order'),
    path('staff_delete_check/<int:id>', views.staff_delete_check, name='staff_delete_check'),
    path('staffchange_status/', views.staffchange_status, name='staffchange_status'),
    path('chk_otp/<int:id>', views.chk_otp, name='chk_otp'),

    
    
    
]