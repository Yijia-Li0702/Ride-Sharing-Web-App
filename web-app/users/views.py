from __future__ import  unicode_literals
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from django.views import View
from shareddriver.models import User
# Create your views here.
#def login_view(request):
   # return render(request, 'register.html')

#from models import *

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        username = request.POST.get('username', '')
        pwd = request.POST.get('pwd', '')

        email = request.POST.get('email','')

        #user = UserInfo.objects.create(username=username, pwd=pwd)
        if username and pwd and email:
            #create model obejects
            user = User(username = username, pwd=pwd, email=email)

            #insert in database
            user.save()
        #if user:
            #return HttpResponse('True')
            return HttpResponseRedirect('/users/login/')


        return HttpResponseRedirect('/users/register/')


class CheckUsernameView(View):
    def get(self, request):
        username = request.GET.get('username', '')

        userList = User.objects.filter(username = username)
        flag = False
        if userList:
            flag = True
        return JsonResponse({'flag' :flag})


def index_view(request):
    return render(request,"login.html")

class LoginView(View):


    def get(self, request):
        return render(request, 'login.html')
    def post(self,request):
        username = request.POST.get('username','')
        pwd = request.POST.get('pwd', '')
        user = User.objects.filter(username=username, pwd=pwd).first()
        #user = User.objects.get(username=username, pwd=pwd)
        #userList =User.objects.filter(username=username, pwd=pwd)
        #if userList:
        #    request.session['users']=userList[0]

        if user:

            user_id = user.id
            
            request.session["username"] = username
           


            return render(request,'homePage.html', {'user_id': user_id})
        else:
            message = "The username does not exist! or The password is wrong!"
            return render(request, 'login.html', {'message': message})






def existView(request):
    #receive parameter
    username = request.GET.get('username', '')
    userList = User.objects.filter(username = username)
    if userList:
        return JsonResponse({'flag':True})

    return JsonResponse({'flag':False})


##########################
def onlyemailView(request):
    email = request.GET.get('email','')
    emailList = User.objects.filter(email = email)
    if emailList:
        return JsonResponse({'flag':True})
    return JsonResponse({'flag':False})


#######################
def LogoutView(request):
    try:
        del request.session["username"]
    except KeyError:
        pass

    return render(request,'login.html')


# class LoginView(View):


#     def get(self, request):
#         return render(request, 'login.html')
#     def post(self,request):
#         username = request.POST.get('username','')
#         pwd = request.POST.get('pwd', '')
#         #user = User.objects.get(username=username, pwd=pwd)
#         # user =  get_object_or_404(User, username = username, pwd = pwd)
#         user = User.objects.get(username=username, pwd=pwd)
#         user_id = user.id

#         # if user:
#         #     request.session['user'] = userList[0]
#         #     user=User.objects.get(username=username)
#             #########################get value from session

#         return render(request,'homePage.html',{'user_id':user_id})
#         # else:
#             # message = "The username does not exist! or The password is wrong!"
#             # return render(request, 'login.html', {'message': message})

#         #return render(request,'login.html',{'message':message})
#         #return render(request, 'login.html',{'context1':context1},{'context2':context2})

def userInfo(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method=="GET":
        return render(request,'userInfo.html',{'user':user,'user_id':user_id})
    if request.method=="POST":
        username=request.POST.get('username','')
        pwd = request.POST.get('pwd','')
        email=request.POST.get('email','')
        user.username = username
        user.pwd = pwd
        user.email = email
        user.save()
        return render(request, 'login.html')




