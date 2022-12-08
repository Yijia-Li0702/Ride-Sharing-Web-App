from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import User, Vehicle, Ride
from django.shortcuts import  render
from django.views import View
from django.db.models import Q
from datetime import datetime
######################

from django.core.mail import send_mail
from django.db.models import Q




# def login_view(request):
#     return render(request, 'login.html')

def homePage(request, user_id):
    return render(request,'homePage.html', {'user_id':user_id})

#be owner of a ride
def requestRide(request, user_id):
    context={}
    user = get_object_or_404(User, pk=user_id)
    context = {'user_id':user_id, 'user' : user}
    if request.method == "POST":
      vehicle_type = request.POST["vehicle_type"]
      destination = request.POST["destination"]
      num_of_passenger= request.POST["num_of_passenger"]
      status = "open"
      ifShared = request.POST.get('ifShared',False)
      spec_ride_req = request.POST["spec_ride_req"]
      # date = request.POST["date"]
      # time = request.POST["time"]
      date_time = request.POST["date_time"]
      editable = True
      if vehicle_type == "X":
        vehicle_capacity = 3
      elif vehicle_type =="XL":
        vehicle_capacity = 4
      elif vehicle_type =="vip":
        vehicle_capacity = 5
      elif vehicle_type =="vvip":
        vehicle_capacity = 6
      check = checkLegal(num_of_passenger, destination, datetime.strptime(date_time, "%Y-%m-%dT%H:%M"), vehicle_capacity)
      if check:
        # ride = Ride.objects.create(vehicle_type=vehicle_type,date=datetime.strptime(date, "%Y-%m-%d"), time=datetime.strptime(time, "%H:%M"),destination=destination,
        # num_of_passenger=num_of_passenger,status=status,editable=editable,vehicle_capacity=vehicle_capacity,ifShared=ifShared,spec_ride_req=spec_ride_req)
        ride = Ride.objects.create(vehicle_type=vehicle_type,date_time=datetime.strptime(date_time, "%Y-%m-%dT%H:%M"), destination=destination, num_of_passenger=num_of_passenger,status=status,editable=editable,vehicle_capacity=vehicle_capacity,ifShared=ifShared,spec_ride_req=spec_ride_req)

        ride.owner = user
        ride.save()
        user.save()
        context['ride'] = ride
        context['ride_id'] = ride.id
      context["check"] = check
      return render(request, 'ride_infm.html', context)
    else:
     return render(request, 'requestRide.html', context)
"""
 #be owner of a ride   
def requestRide(request, user_id):
    context={}
    #user = get_object_or_404(User, pk=user_id)
    user = verify_user_session(request, user_id)
    if user is not None:
        context = {'user_id':user_id, 'user' : user}
        if request.method == "POST":
            vehicle_type = request.POST["vehicle_type"]
            destination = request.POST["destination"]
            num_of_passenger= request.POST["num_of_passenger"]
            status = "open"
            ifShared = request.POST.get('ifShared',False)
            spec_ride_req = request.POST["spec_ride_req"]
            # date = request.POST["date"]
            # time = request.POST["time"]
            date_time = request.POST["date_time"]
            editable = True
            if vehicle_type == "X":
                vehicle_capacity = 3
            elif vehicle_type =="XL":
                vehicle_capacity = 4
            elif vehicle_type =="vip":
                vehicle_capacity = 5
            elif vehicle_type =="vvip":
                vehicle_capacity = 6
            check = checkLegal(num_of_passenger, destination, datetime.strptime(date_time, "%Y-%m-%dT%H:%M"), vehicle_capacity)
            if check:
        # ride = Ride.objects.create(vehicle_type=vehicle_type,date=datetime.strptime(date, "%Y-%m-%d"), time=datetime.strptime(time, "%H:%M"),destination=destination,
        # num_of_passenger=num_of_passenger,status=status,editable=editable,vehicle_capacity=vehicle_capacity,ifShared=ifShared,spec_ride_req=spec_ride_req)
                ride = Ride.objects.create(vehicle_type=vehicle_type,date_time=datetime.strptime(date_time, "%Y-%m-%dT%H:%M"), destination=destination, num_of_passenger=num_of_passenger,status=status,editable=editable,vehicle_capacity=vehicle_capacity,ifShared=ifShared,spec_ride_req=spec_ride_req)

                ride.owner = user
                ride.save()
                user.save()
                context['ride'] = ride
                context['ride_id'] = ride.id
            context["check"] = check
            return render(request, 'ride_infm.html', context)
        else:
            return render(request, 'requestRide.html', context)
     else:
          return render(request, 'login.html')
 """

def checkLegal(num_of_passenger, destination, date_time, vehicle_capacity):
  if int(num_of_passenger) > vehicle_capacity:
    return False
  if destination == '':
    return False
  if date_time < datetime.now():
    return False
  return True
#user as a owner of ride, show information of the ride, can edit unconfirm ride
def ride_infm(request, user_id, ride_id):
    context={}
    user = get_object_or_404(User, pk=user_id)
    ride = get_object_or_404(Ride, pk=ride_id)
    context = {'user_id':user_id, 'user' : user, 'ride' : ride, 'ride_id' : ride_id}
    context["check"] = True
    if request.method == "POST":
      ride.vehicle_type = request.POST["vehicle_type"]
      ride.destination = request.POST["destination"]
      ride.num_of_passenger = request.POST["num_of_passenger"] 
      #status = "open"
      ride.ifShared = request.POST.get('ifShared',False)
      ride.spec_ride_req = request.POST["spec_ride_req"]
      # ride.date = request.POST["date"]
    	# ride.time = request.POST["time"]
      date_time = request.POST["date_time"]
      ride.date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
      check = checkLegal(ride.num_of_passenger, ride.destination, ride.date_time, ride.vehicle_capacity)
      if check:
        ride.save()
      context["check"] = check
      return render(request, 'ride_infm.html', context)
    else:
    	return render(request, 'ride_infm.html', context)	 

#show all rides as owner and sharer
def selectRides(request, user_id):
    context={}
    user = get_object_or_404(User, pk=user_id)
    myRide = Ride.objects.filter(Q(owner = user)|Q(sharer__id__exact=user.id))
    context = {'user_id':user_id, 'user' : user, 'myRide':myRide}
    return render(request,'selectRides.html', context)


def shareRide(request, user_id):
    context={}
    user = get_object_or_404(User, pk=user_id)
    context= {'user_id':user_id, 'user' : user}
    context["check"] = True
    if request.method == "POST":
      vehicle_type = request.POST["vehicle_type"]
      destination = request.POST["destination"]
      required_num_of_passenger = request.POST["num_of_passenger"] 
      #  ear_date = request.POST["ear_date"]
      #  ear_time = request.POST["early_time"]
  	  # late_date = request.POST["late_date"]
      #  late_time = request.POST["late_time"]
      ear_date_time = request.POST["ear_date_time"]
      late_date_time = request.POST["late_date_time"]
      check = checkTimeLegal(ear_date_time,late_date_time)
      context["check"] = check
      # UsableRide = Ride.objects.filter(Q(vehicle_type=vehicle_type)&Q(destination=destination)&Q(date=date)&Q(time__lte =late_time)&Q(time__gte=ear_time)
      # &Q(ifShared=True)&Q(status="open")).exclude(owner = user).exclude(sharer__id__exact=user.id).exclude(driver__id__exact=user.id)
      UsableRide = Ride.objects.filter(Q(vehicle_type=vehicle_type)&Q(destination=destination)&Q(date_time__lte =late_date_time)&Q(date_time__gte=ear_date_time)&Q(ifShared=True)&Q(status="open")).exclude(owner = user).exclude(sharer__id__exact=user.id).exclude(driver__id__exact=user.id)

      for ride in UsableRide :
        if (ride.vehicle_capacity-ride.num_of_passenger) < int(required_num_of_passenger):
          UsableRide.exclude(id=ride.id) 
          
      context["UsableRide"]= UsableRide
      context["required_num_of_passenger"]=required_num_of_passenger
      context["operation"] = "showInformation"
      return render(request,'shareRide.html', context)
    else:
      context["operation"] = "fillInformation"
      return render(request,'shareRide.html', context)

def checkTimeLegal(ear_date_time,late_date_time):
  ear = datetime.strptime(ear_date_time, "%Y-%m-%dT%H:%M")
  late =  datetime.strptime(late_date_time, "%Y-%m-%dT%H:%M")
  if ear < datetime.now():
    return False
  if late < datetime.now():
    return False
  if ear > late:
    return False
  return True


def shareRideCnfm(request, user_id, ride_id):
    user = get_object_or_404(User, pk=user_id)
    ride = get_object_or_404(Ride, pk=ride_id) 
    context = {'user_id':user_id, 'user' : user, 'ride' : ride, 'ride_id' : ride_id}
    context["check"] = True
    if request.method == "POST":
      ride.num_of_passenger=ride.num_of_passenger+int(request.POST["required_num_of_passenger"])
      ride.editable = False
      ride.sharer.add(user)
      ride.save()
      return render(request, 'ride_infm.html', context)
    else:
      return render(request, 'ride_infm.html', context)

 
#########################################################################
"""
def driverReg(request, user_id):
    context = {}
    user = get_object_or_404(User, pk=user_id)
    #user.ifDriver = True
    user.save()
    ##########
    if user.ifDriver==True:
    ##########
        if request.method == "POST":
            # drivername = request.POST.get('drivername', '')
            type = request.POST.get('vehicle_type', '')
            # lnumber = request.POST.get('lnumber', '')
            # maxnum = request.POST.get('maxnum', '')
            if type == "X":
                maxnum = 3
            elif type == "XL":
                maxnum = 4
            elif type == "vip":
                maxnum = 5
            elif type == "vvip":
                maxnum = 6
            append = request.POST.get('append', '')

            # ride_list = Ride.objects.filter(vehicle_type=type, num_of_passenger__range=(1,maxnum), spec_ride_req=append, status="open",
            #                             ).exclude(owner=user)
            ride_list = Ride.objects.filter(vehicle_type=type, num_of_passenger__range=(1,maxnum), spec_ride_req=append, status="open").exclude(owner=user).exclude(sharer=user)



            return render(request, "driverReg.html", {"ride_list": ride_list, "user_id": user_id}, )
        if request.method=="GET":
            return render(request, "driverReg.html", { "user_id": user_id}, )
    else:

         return render(request, "driver_register_Info.html",{"user_id":user_id})
"""
def driverReg(request, user_id):
    context = {}
    user = get_object_or_404(User, pk=user_id)
    #user.ifDriver = True
    user.save()
    ##########
    if user.ifDriver==True:
    ##########
        

        if request.method == "POST":
            vehicle = Vehicle.objects.get(driver=user)
            type = vehicle.vehicle_type;
            #type = request.POST.get('vehicle_type', '')

            if type == "X":
                maxnum = 3
            elif type == "XL":
                maxnum = 4
            elif type == "vip":
                maxnum = 5
            elif type == "vvip":
                maxnum = 6

        
            ride_list = Ride.objects.filter(vehicle_type=type, num_of_passenger__range=(1,maxnum), spec_ride_req=vehicle.spec_veh_info, status="open",
                                        ).exclude(owner=user).exclude(sharer=user)


            return render(request, "driverReg.html", {"ride_list": ride_list, "user_id": user_id}, )
        if request.method=="GET":
            return render(request, "driverReg.html", { "user_id": user_id}, )
    else:

         return render(request, "driver_register_Info.html",{"user_id":user_id})


def driver_Register_Info(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method=="GET":
        return render(request, "driver_register_Info.html",{"user_id":user_id})
    if request.method=="POST":
        #vehicle_type = request.POST.get('vehicle_type', '')
        vehicle_type = request.POST.get('vehicle_type', '')
        # lnumber = request.POST.get('lnumber', '')
        # maxnum = request.POST.get('maxnum', '')

        if vehicle_type == "X":
            max_num = 3
        elif vehicle_type == "XL":
            max_num = 4
        elif vehicle_type == "vip":
            max_num = 5
        elif vehicle_type == "vvip":
            max_num = 6
        license_num = request.POST.get('license_num', '')
        #max_num = request.POST.get('max_num', '')
        spec_veh_info = request.POST.get('spec_veh_info', '')
        ifDriver = request.POST.get('ifDriver', '')
        user.ifDriver = ifDriver
        user.save()
        vehicle = user.vehicle.create(driver=user_id, vehicle_type=vehicle_type,
                                      license_num=license_num, max_num=max_num, spec_veh_info=spec_veh_info)
        vehicle.save()
        return render(request, 'driverInfo.html', {'user_id': user_id, 'user': user , 'vehicle_id':vehicle.id , 'vehicle':vehicle})


def myCurrentOrder(request, user_id, ride_id):
    if request.method=="GET":
        user = get_object_or_404(User, pk=user_id)
        ride = get_object_or_404(Ride, pk=ride_id)
        ##############################################
        #ride.owner.email
        ###############################################
        check_email(ride.owner.email)
        #try:
            #sharer = User.objects.get(username=ride.sharer)
        for s in ride.sharer.all():
            check_email(s.email)
        #except:
         #   pass
        ride.status = "Confirm"
        ride.driver = User.objects.filter(username=user.username).first()
        ride.save()

        #ride.save()
        context = {'user': user, 'user_id': user_id, 'ride': ride, 'ride_id': ride_id}

        return render(request, 'order_info.html',context )
    if request.method=="POST":
        user = get_object_or_404(User, pk=user_id)
        ride = get_object_or_404(Ride, pk=ride_id)
        ride.status = "Complete"
        ride.save()
        return render(request,'homePage.html',{'user_id':user_id})



def myOrder(request, user_id):
    if request.method=="GET":
        user = get_object_or_404(User, pk=user_id)
        ride_list=Ride.objects.filter(driver=user_id)
        return render(request, "totalOrder.html", {"ride_list": ride_list, "user_id": user_id}, )




def orderComplete(request,user_id,ride_id):
    if request.method=="GET":
        user = get_object_or_404(User, pk=user_id)
        ride = get_object_or_404(Ride, pk=ride_id)
        ride.status="Complete"
        ride.save()
        return  render(request,'orderComplete.html',{'user_id':user_id})


#########################
#import the email module

from django.core.mail import send_mail
from django.conf import settings
def check_email(str):
    #send_mail()

    send_mail(subject="The notification of shareddriver",
            message="The ride has been confirmed!", from_email=settings.EMAIL_HOST_USER,
             recipient_list=[str]
             )




def driverInfo(request, user_id):

    context = {}
    user = get_object_or_404(User, pk=user_id)
    user.username = user.username
    user.email = user.email

    context = {'user_id': user_id, 'user': user}
    if request.method == "POST":
        vehicle_type =request.POST.get('vehicle_type', '')
        license_num = request.POST.get('license_num', '')
        #max_num = request.POST.get('max_num', '')
        if vehicle_type == "X":
            max_num = 3
        elif vehicle_type == "XL":
            max_num = 4
        elif vehicle_type == "vip":
            max_num = 5
        elif vehicle_type == "vvip":
            max_num = 6
        spec_veh_info = request.POST.get('spec_veh_info', '')
        ifDriver = request.POST.get('ifDriver','')
        ########################
        #vehicle = Vehicle.objects.filter(driver=user_id)
        #vehicle.delete()
        if ifDriver:
            user.ifDriver=ifDriver

            vehicle=Vehicle.objects.get(driver=user_id)

            vehicle.vehicle_type=vehicle_type
            vehicle.license_num=license_num
            vehicle.max_num=max_num
            vehicle.spec_veh_info=spec_veh_info
            vehicle.save()


        ##############
            return render(request, 'driverInfo.html', {'user_id': user_id, 'user': user , 'vehicle_id':vehicle.id , 'vehicle':vehicle})
        else:
            user.ifDriver=ifDriver
            user.save()
            vehicle=Vehicle.objects.filter(driver=user_id)
            vehicle.delete()
            return render(request,'homePage.html',{'user_id':user_id})
    else:
        #vehicle = Vehicle.objects.filter(driver=user_id)
        #vehicle.delete()
        user=User.objects.get(pk=user_id)
        vehicle = Vehicle.objects.get(driver=user_id)

        return render(request, 'driverInfo.html', {'user_id': user_id, 'user': user,'vehicle_id':vehicle.id , 'vehicle':vehicle})
# #there input the information of the vehicle, and show all satisfied order



def verify_user_session(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    username = request.session.get("username", "")
    
    if user.username == username:
        return user
    else:
        return None




# def driverReg(request, user_id):
#     context = {}
#     user = get_object_or_404(User, pk=user_id)
#     #user.ifDriver = True
#     user.save()
#     if request.method == "POST":
#         #drivername = request.POST.get('drivername', '')
#         type = request.POST.get('type', '')
#         #lnumber = request.POST.get('lnumber', '')
#         # maxnum = request.POST.get('maxnum', '')
#         if type == "X":
#           maxnum = 3
#         elif type =="XL":
#           maxnum = 4
#         elif type =="vip":
#           maxnum = 5
#         elif type =="vvip":
#           maxnum = 6
#         append = request.POST.get('append', '')

#         ride_list = Ride.objects.filter(vehicle_type=type, num_of_passenger__range=(1,maxnum), spec_ride_req=append, status="open",
#                                         ).exclude(owner=user)
#         return render(request, "driverReg.html", {"ride_list": ride_list, "user_id": user_id}, )
#     else:
#         return render(request, "driverReg.html",{"user_id":user_id})

# def myCurrentOrder(request, user_id, ride_id):
#     if request.method=="GET":
#         user = get_object_or_404(User, pk=user_id)
#         ride = get_object_or_404(Ride, pk=ride_id)
#         #ride.status = "Confirm" 需要改变状态
#         context = {'user': user, 'user_id':user_id, 'ride': ride, 'ride_id': ride_id}
#         #check_email();

#         ride.status = "Confirm"
#         ride.save()
#         context = {'user': user, 'user_id': user_id, 'ride': ride, 'ride_id': ride_id}

#         return render(request, 'order_info.html', context)
#     if request.method=="POST":
#         user = get_object_or_404(User, pk=user_id)
#         ride = get_object_or_404(Ride, pk=ride_id)
#         ride.status = "Complete"
#         ride.save()
#         return render(request,'homePage.html',{'user_id':user_id})



# def myOrder(request, user_id):
#     if request.method=="GET":
#         user = get_object_or_404(User, pk=user_id)
#         ride_list=Ride.objects.filter(driver=user_id)
#         return render(request, "totalOrder.html", {"ride_list": ride_list, "user_id": user_id}, )


# def driverInfo(request, user_id):

#     context = {}
#     user = get_object_or_404(User, pk=user_id)
#     user.username = user.username
#     user.email = user.email

#     context = {'user_id': user_id, 'user': user}
#     if request.method == "POST":
#         vehicle_type =request.POST.get('vehicle_type', '')
#         license_num = request.POST.get('license_num', '')
#         # max_num = request.POST.get('max_num', '')
#         if vehicle_type == "X":
#           max_num = 3
#         elif vehicle_type =="XL":
#           max_num = 4
#         elif vehicle_type =="vip":
#           max_num = 5
#         elif vehicle_type =="vvip":
#           max_num = 6
#         spec_veh_info = request.POST.get('spec_veh_info', '')
#         ifDriver = request.POST.get('ifDriver','')
#         ########################
#         #delete = Vehicle.objects.filter(driver=user_id)
#         #delete.delete()

#         user.ifDriver=ifDriver

#         vehicle=Vehicle.objects.get(driver=user_id)
#         if vehicle:
#           vehicle.vehicle_type=vehicle_type
#           vehicle.license_num=license_num
#           vehicle.max_num=max_num
#           vehicle.spec_veh_info=spec_veh_info
#           vehicle.save()
#           #Vehicle.objects.filter(driver=user_id).update(vehicle_type=vehicle_type,
#                             #license_num=license_num,max_num=max_num,spec_veh_info=spec_veh_info)
#           #vehicle.save()
#         #####################check license
#         else:
#           vehicle = user.vehicle.create(driver=user_id, vehicle_type=vehicle_type,
#                                           license_num=license_num, max_num=max_num, spec_veh_info=spec_veh_info)
#           vehicle.save()

#         #####################################
#         #vehicle = user.vehicle.create(driver=user.username, vehicle_type=vehicle_type,
#                             #license_num=license_num,max_num=max_num,spec_veh_info=spec_veh_info)


#         ##############
#         return render(request, 'driverInfo.html', {'user_id': user_id, 'user': user , 'vehicle_id':vehicle.id , 'vehicle':vehicle})
#     else:
#         user=User.objects.get(pk=user_id)
#         vehicle = Vehicle.objects.get(driver=user_id)

#         return render(request, 'driverInfo.html', {'user_id': user_id, 'user': user,'vehicle_id':vehicle.id , 'vehicle':vehicle})
        

#######################################myself########################################
# def driverReg(request, user_id):
#     context={}
#     user = get_object_or_404(User, pk=user_id)
#     context["ifDriver"] = user.ifDriver
#     context["user"] = user
#     context["user_id"] = user_id
#     return render(request, 'driverReg.html', context)

# def editDriverInfo(request, user_id):
#     context={}
#     user = get_object_or_404(User, pk=user_id)
#     context["ifDriver"] = user.ifDriver
#     context["user"] = user
#     context["user_id"] = user_id
#     if not user.ifDriver:
#       vehicle = None   
#     else:
#       vehicle = list(user.vehicle.all())[0]
#     context["vehicle"]=vehicle
#     #if not user.ifDriver:
#     if request.method == "POST":
#         vehicle_type = request.POST["vehicle_type"]
#         license_num = request.POST["license_num"]
#         if vehicle_type == "X":
#           max_num = 3
#         elif vehicle_type =="XL":
#           max_num = 4
#         elif vehicle_type =="vip":
#           max_num = 5
#         elif vehicle_type =="vvip":
#           max_num = 6
#         #max_num = request.POST["max_num"]
#         spec_veh_info = request.POST["spec_veh_info"]
#         if not user.ifDriver:
#           user.ifDriver = True
#           user.vehicle.create(vehicle_type=vehicle_type,license_num=license_num,max_num=max_num,spec_veh_info=spec_veh_info)
#         else:
#           vehicle = list(user.vehicle.all())[0]
#           vehicle.vehicle_type=vehicle_type
#           vehicle.license_num = license_num
#           if vehicle.vehicle_type == "X":
#             vehicle.max_num = 3
#           elif vehicle_type =="XL":
#             vehicle.max_num = 4
#           elif vehicle_type =="vip":
#             vehicle.max_num = 5
#           elif vehicle_type =="vvip":
#             vehicle.max_num = 6
#           vehicle.spec_veh_info=spec_veh_info
#           vehicle.save()
#         user.save()
#         return render(request, 'homePage.html', {'user_id':user_id})
#     else:
#         return render(request,'editDriverInfo.html',context)
        

