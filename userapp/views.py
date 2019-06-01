from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth.models import User
# Create your views here.

# def base(request):
#     return render(request,'userapp/base.html',)

def index(request):
    return render(request,'userapp/index.html')


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
