from django.shortcuts import render
from app.models import *
from app.forms import *
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.



def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)

        if ufd.is_valid() and pfd.is_valid():
            MUFDO=ufd.save(commit=False)
            pw=ufd.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()

            MPFDO=pfd.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            send_mail('Registration Done with Weather_API',
                      
            '''Thank you for Registration you have successfully register in Weather_API your welcome..! Search your location in the page...!
            The Easiest Weather API -
                       Query Global Weather Data for Free Integrate weather into your applications with the easiest-to-use global weather API including historical weather data, current conditions, up-to-date forecasts, and historical forecast information.
             
                       Try our single-endpoint forecast and weather history API for free to see why more businesses, developers, and analysts choose Visual Crossing..
                       
                               1.Historical Weather
                        Correlate existing business data with over 50 years of historical weather reports for every location on the Earth.
                               2.Forecast & Current Conditions
                        Schedule your activities and your business using current weather data and our global blended 15-day forecast.
                               3.Historical Forecast
                        Gain insight into customer behavior using the exact forecast that your customers saw on the day that they make their plans.
                               4.Statistical Forecast
                        Understand future weather conditions beyond the 15-day model-based forecast using statistical patterns and climate normals.''',

            'sainarendra62645@gmail.com',
            [MUFDO.email],
            fail_silently=False,
            )

            return HttpResponse('<center><h1>Registartion Is Successfull')
        else:
            return HttpResponse('<center><h1>Invalid Data')

    return render(request,'registration.html',d)





def user_login(request):
    if request.method == 'POST':
        un = request.POST['un']
        pw = request.POST['pw']
        AUO = authenticate(username=un,password=pw)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username'] = un
            return HttpResponseRedirect(reverse('dummy'))
        else:
            return HttpResponse('<center><h1>Invalid credentials please try again...')
        
    return render(request,'user_login.html')





def dummy(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'dummy.html',d)
    
    return render(request,'dummy.html')





@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse('dummy'))






@login_required
def profile_display(request):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    PO = Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}

    return render(request,'profile_display.html',d)





@login_required
def search(request):
    if request.method=='POST':
        city_name=request.POST['city']
        api_key = '30d4741c779ba94c470ca1f63045390a'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
        response = requests.get(url)
        weather_data = response.json()
        print(weather_data)
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather=weather_data['main']['feels_like']
        speed=weather_data['wind']['speed']
        username=request.session.get('username')
        LUO=User.objects.get(username=username)
        obj=WeatherData.objects.get_or_create(username=LUO,city=city_name, temperature=temperature, humidity=humidity,weather=weather, speed=speed)[0]
        obj.save()
        d={'obj':obj}
        return render(request,'search.html',d)
    return render(request,'search.html')




def all_history(request):
    LOW = WeatherData.objects.all()
    d = {'LOW': LOW}
    return render(request,'all_history.html',d)





@login_required
def user_history(request):
    username = request.session['username']
    UO = User.objects.get(username=username)
    LOW = WeatherData.objects.filter(username=UO)
    d={'LOW':LOW}
    return render(request,'user_history.html',d)






def reset_password(request):

    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']

        LUO=User.objects.filter(username=un)

        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponseRedirect(reverse('user_login'))
        else:
            return HttpResponse('<center><h1>User is not present in my DataBase')
    return render(request,'reset_password.html')




@login_required
def change_password(request):
    if request.method == 'POST':
        password = request.POST['pw']
        password2 = request.POST['pw2']
        if password == password2:
            un = request.session.get('username')
            UO = User.objects.get(username=un)
            UO.set_password(password)
            UO.save()
            return HttpResponse('<center><h1>Password change successfully')
        else:
            return HttpResponse('<center><h1>Password and Re-Password not match')
    
    return render(request,'change_password.html')