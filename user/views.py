# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib import messages, auth


# # Create your views here.
# def register(request):
#     context = {}
#     if request.method == 'POST':
#      return redirect('/login/')
#     return render(request, 'user/register.html', context)

# def store(request):
#    fname = request.POST['first_name']
#    lname = request.POST['last_name']
#    email = request.POST['email']
#    username = request.POST['username']
#    password = request.POST['psw']
#    reppass = request.POST['psw-repeat']

# #    velodation that psw and reppsw same or not
#    if password == reppass:
#       User.objects.create_user(first_name = fname, last_name = lname, email = email, username=username, password=password)
#       return redirect('/user/login')
#    else:
#       messages.success(request, "password not matched")
#       return redirect('/user/register')
      

# def login(request):
#     context = {}
#     return render(request, 'user/login.html', context)

# def login_check(request):
#    username = request.POST['username']
#    password = request.POST['psw']

#    result = auth.authenticate(username = username , password = password)
#    if result is None:
#       messages.success(request, "invalid details")

#       return redirect('/user/login')
#    else:
#        auth.login(request, result)  # Log the user in
#        return redirect('/user/home/')  # Or wherever you want after login
#       # return redirect('/user/register')
# def home(request):
#     context = {}
#     return render(request, 'user/home.html', context)







from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_protect


def register(request):
    context = {}
    if request.method == 'POST':
        return redirect('/user/store')
    return render(request, 'user/register.html', context)

def store(request):
    fname = request.POST['first_name']
    lname = request.POST['last_name']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['psw']
    reppass = request.POST['psw-repeat']

    if password == reppass:
        User.objects.create_user(first_name=fname, last_name=lname, email=email, username=username, password=password)
        return redirect('/user/login/')
    else:
        messages.error(request, "Passwords do not match")
        return redirect('/user/register/')

def login_view(request):
    context = {}
    return render(request, 'user/login.html', context)

def login_check(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        result = auth.authenticate(username=username, password=password)
        if result is None:
            messages.error(request, "Invalid login details")
            return redirect('/user/login/')
        else:
            auth.login(request, result)
            return redirect('/user/home/')
    else:
        return redirect('/user/login/')

def home(request):
    context = {}
    return render(request, 'user/home.html', context)

def email_send(request):
   to = request.POST['email']
   subject = request.POST['subject']
   message = request.POST['message']
   file = request.FILES.get('file')
   
   email = EmailMessage(subject=subject, body=message, from_email=settings.EMAIL_HOST_USER, to=[to])
   # email.attach(file.name,file.read(), file.content_type )
   # email.send()
   if file:
        email.attach(file.name, file.read(), file.content_type)

   email.send()

   messages.success(request, "Email sent successfully!")  # ✅ Add this line
   return redirect('/user/home')

def logout(request):
    auth.logout(request)
    return redirect('/user/register')