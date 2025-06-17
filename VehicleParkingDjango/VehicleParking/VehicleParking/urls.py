
from django.contrib import admin
from django.urls import path
from vehicle.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Index,name='index'),
path('about',about,name='about'),
path('contact',contact,name='contact'),
path('admin_login',admin_login,name='admin_login'),
path('admin_home',admin_home,name='admin_home'),
path('logout',Logout,name='logout'),
path('add_category',add_category,name='add_category'),
    path('manage_category',manage_category,name='manage_category'),
path('delete_category/<int:pid>', delete_category,name='delete_category'),
path('edit_category/<int:pid>',edit_category,name='edit_category'),
path('add_vehicle',add_vehicle,name='add_vehicle'),
path('manage_incomingvehicle',manage_incomingvehicle,name='manage_incomingvehicle'),
path('view_incomingdetail/<int:pid>',view_incomingdetail,name='view_incomingdetail'),
path('manage_outgoingvehicle',manage_outgoingvehicle,name='manage_outgoingvehicle'),
path('view_outgoingdetail/<int:pid>',view_outgoingdetail,name='view_outgoingdetail'),
    path('print/<int:pid>',print_detail,name='print'),
path('search',search,name='search'),
path('betweendate_report',betweendate_report,name='betweendate_report'),
    path('betweendate_reportdetails',betweendate_reportdetails,name='betweendate_reportdetails'),
]
