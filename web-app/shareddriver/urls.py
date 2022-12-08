from django.urls import path
from.import views
from .models import User, Vehicle, Ride
 
app_name = 'shareddriver'
urlpatterns = [
 #path('', views.login_view),
 path('<int:user_id>/', views.homePage,name='homePage'),
 #path('<int:user_id>/driverReg/', views.driverReg,name='driverReg'),
 path('<int:user_id>/requestRide/', views.requestRide,name='requestRide'),
 path('<int:user_id>/selectRides/', views.selectRides,name='selectRides'),
 path('<int:user_id>/shareRide/', views.shareRide,name='shareRide'),
 #path('<int:user_id>/editDriverInfo/', views.editDriverInfo,name='editDriverInfo'),
 path('<int:user_id>/<int:ride_id>/ride_infm/', views.ride_infm, name='ride_infm'),
 path('<int:user_id>/<int:ride_id>/shareRideCnfm/', views.shareRideCnfm, name='shareRideCnfm'),
 ##############################################################################
 path('<int:user_id>/driver_Register_Info/', views.driver_Register_Info,name='driver_Register_Info'),

 path('<int:user_id>/<int:ride_id>/orderComplete/', views.orderComplete, name='orderComplete'),
 path('<int:user_id>/driverReg/', views.driverReg,name='driverReg'),

 path('<int:user_id>/<int:ride_id>/myCurrentOrder/',views.myCurrentOrder,name='myCurrentOrder'),

 path('<int:user_id>/driverReg/personalInfo/',views.driverInfo,name='personalInfo'),

 path('<int:user_id>/myOrder/',views.myOrder,name='myOrder')





]



#from django.urls import path
#
#from . import views
#
#urlpatterns = [
#    path('', views.index, name='index'),
#]
