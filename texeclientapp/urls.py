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
    #--------------------------------------------------------User Module
    path('user_regi/', views.user_regi, name='user_regi'),
    
]