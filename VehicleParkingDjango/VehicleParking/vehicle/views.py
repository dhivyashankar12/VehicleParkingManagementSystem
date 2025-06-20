from django.db.models import Q #queries
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import date
from datetime import datetime, timedelta, time
import random
from django.utils import timezone

# Create your views here.

def Index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request,user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'admin_login.html', d)


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    today = datetime.now().date()
    yesterday = today - timedelta(1)
    lasts = today - timedelta(7)

    tv = Vehicle.objects.filter(pdate=today).count()
    yv = Vehicle.objects.filter(pdate=yesterday).count()
    ls = Vehicle.objects.filter(pdate__gte=lasts,pdate__lte=today).count()
    totalv = Vehicle.objects.all().count()

    d = {'tv':tv,'yv':yv,'ls':ls,'totalv':totalv}
    return render(request,'admin_home.html',d)


def Logout(request):
    logout(request)
    return redirect('index')


def add_category(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method=="POST":
        cn = request.POST['categoryname']
        sc = request.POST.get('slotcount', 0)

        try:
            Category.objects.create(categoryname=cn, slot_count=int(sc))
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'add_category.html', d)

def manage_category(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.all()
    d = {'category':category}
    return render(request, 'manage_category.html', d)


def delete_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('manage_category')

def edit_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    category = Category.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        cn = request.POST['categoryname']
        sc = request.POST.get('slotcount', 0)
        category.categoryname = cn
        category.slot_count = int(sc)
        try:
            category.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'category':category}
    return render(request, 'edit_category.html',d)

def add_vehicle(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    category1 = Category.objects.all()
    if request.method=="POST":
        pn = str(random.randint(10000000, 99999999))
        ct = request.POST['category']
        vc = request.POST['vehiclecompany']
        rn = request.POST['regno']
        on = request.POST['ownername']
        oc = request.POST['ownercontact']
        pd_str = request.POST['pdate']
        it_str = request.POST['intime']
        status = "In"

        try:
            date_part = datetime.strptime(pd_str, '%Y-%m-%d').date()
            time_part = datetime.strptime(it_str, '%H:%M').time()
            it = timezone.make_aware(datetime.combine(date_part, time_part))
        except ValueError:
            error = "yes"
            it = None
        
        if it:
            try:
                category = Category.objects.get(categoryname=ct)
                if category.current_slot < category.slot_count:

                    Vehicle.objects.create(
                        parkingnumber=pn,
                        category=category,
                        vehiclecompany=vc,
                        regno=rn,
                        ownername=on,
                        ownercontact=oc,
                        pdate=pd_str,
                        intime=it,
                        outtime=None,
                        parkingcharge='',
                        remark='',
                        status=status
                    )
                    category.current_slot +=1
                    category.save()
                    error = "no"
                else:
                    error = "Parking full for this category"
            except Exception as e:
                print("Error while adding vehicle:", e)
                error = str(e) 
    
    d = {'error': error, 'category1': category1}
    return render(request, 'add_vehicle.html', d)

def manage_incomingvehicle(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    vehicle = Vehicle.objects.filter(status="In")
    d = {'vehicle':vehicle}
    return render(request, 'manage_incomingvehicle.html', d)

def view_incomingdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_home')
    error = ""
    vehicle = Vehicle.objects.get(id=pid)
    if request.method == 'POST':
        rm = request.POST['remark']
        ot_str = request.POST['outtime']
        try:
            outtime = datetime.strptime(ot_str, '%Y-%m-%dT%H:%M')
            outtime = timezone.make_aware(outtime)

            intime = vehicle.intime
            if timezone.is_naive(intime):
                intime = timezone.make_aware(intime)
            duration = outtime - intime
            hours = int(duration.total_seconds() // 3600)
            if duration.total_seconds() % 3600 > 0:
                hours += 1  

            # Rate by category
            rate_map = {
                "2-Wheeler": 10,
                "4-Wheeler": 20,
                "Truck": 30
            }
            category_name = vehicle.category.categoryname
            rate_per_hour = rate_map.get(category_name, 15)  # default ₹15/hr
            charge = hours * rate_per_hour        
            
            vehicle.remark = rm
            vehicle.outtime = ot_str
            vehicle.parkingcharge = f"₹{charge}"
            vehicle.status = "Out"
            vehicle.save()
            error = "no"
        except Exception as e:
            print("Error:", e)
            error = "yes"

    d = {'vehicle': vehicle,'error':error}
    return render(request,'view_incomingdetail.html', d)


def manage_outgoingvehicle(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    vehicle = Vehicle.objects.filter(status="Out")
    d = {'vehicle':vehicle}
    return render(request, 'manage_outgoingvehicle.html', d)


def view_outgoingdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    vehicle = Vehicle.objects.get(id=pid)

    d = {'vehicle': vehicle}
    return render(request,'view_outgoingdetail.html', d)


def print_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    vehicle = Vehicle.objects.get(id=pid)

    d = {'vehicle': vehicle}
    return render(request,'print.html', d)


def search(request):
    q = None
    if request.method == 'POST':
        q = request.POST['searchdata']
    try:
        vehicle = Vehicle.objects.filter(Q(parkingnumber=q))
        vehiclecount = Vehicle.objects.filter(Q(parkingnumber=q)).count()

    except:
        vehicle = ""
    d = {'vehicle': vehicle,'q':q,'vehiclecount':vehiclecount}
    return render(request, 'search.html',d)


def betweendate_reportdetails(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, 'betweendate_reportdetails.html')



def betweendate_report(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        vehicle = Vehicle.objects.filter(Q(pdate__gte=fd) & Q(pdate__lte=td))
        vehiclecount = Vehicle.objects.filter(Q(pdate__gte=fd) & Q(pdate__lte=td)).count()
        d = {'vehicle': vehicle,'fd':fd,'td':td,'vehiclecount':vehiclecount}
        return render(request, 'betweendate_reportdetails.html', d)
    return render(request, 'betweendate_report.html')