from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth.models import User

# for login..
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

# def base(request):
#     return render(request,'userapp/base.html',)

def index(request):
    return render(request,'userapp/index.html')

@csrf_exempt
def register(request):
    registered= False
    if request.method=="POST":
        user_form= UserForm(data=request.POST)
        profile_form =UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)    #pws saved via hashing
            user.save()

            profile = profile_form.save(commit=False)   #commit=False since we've to check if the pic is there or not before saving it
            profile.user=user   #this is setting the OneToOne relationship in views as it was in models

            # now checking if they provided a profile picture or not
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered =True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form =  UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'userapp/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})


@csrf_exempt
def user_login(request):


    if request.method == 'POST':
        username = request.POST.get('username') #since we've given user name as -->name="username" in login.html
        password = request.POST.get('password')


        user= authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('dashboard'))
                # return HttpResponseRedirect(reverse('index'))

            else:
                # return HttpResponse("Account Not active")
                return HttpResponseRedirect(reverse('user_login'))
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password{}".format(username,password))
            return HttpResponse('invalid login details supplied!')
    else:
        return render(request,'userapp/login.html',{})

@login_required
def special(request):
    return HttpResponse("You are logged in..;-)")



@login_required 
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def dashboard(request):
    return render(request, 'userapp/dashboard.html')
     # HttpResponseRedirect(reverse('dashboard'))
      # HttpResponse('dashboard')
