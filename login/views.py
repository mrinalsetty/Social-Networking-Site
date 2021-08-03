from django.http.response import HttpResponse, HttpResponseRedirect
from login.models import friends, posts, users
from django.shortcuts import redirect, render
from datetime import date, datetime
import math
import random
from django.db import connection
#from django.contrib import messages
#from django.contrib.auth import authenticate, login
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import AuthenticationForm
#from .forms import UserRegisterForm
from django.core.mail import send_mail
#from django.core.mail import EmailMultiAlternatives
#from django.template.loader import get_template
#from django.template import Context
#import mysql.connector
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from social.settings import EMAIL_HOST_USER
from django.contrib.auth import logout as logouts

#from django.http import HttpResponse

# Create your views here.

'''def home(request):
    return HttpResponse('Hello {{}}!..')'''

'''def home(request):
    template=loader.get_template('home.html')
    return HttpResponse(template.render())'''


def home(request):
    '''sub='welcome to django'
    digits = "0123456789"
    otp = ""
    for i in range(6) :
        otp += digits[math.floor(random.random() * 10)]
    message= f"django mail process successful "+otp
    email_from= settings.EMAIL_HOST_USER
    to= ['pavanc0312@gmail.com']
    send_mail( sub,message,email_from,to)'''
    ##################update query###############
    '''name="pavanchan"
    cursor=connection.cursor()
    #cursor.execute("Select count(*) from login_users where username=%s",[name])
    cursor.execute("Update login_users set password='User@123' where username=%s",[name])
    #r = cursor.fetchone()
    print("executed.............................................")'''
    request.session['username'] = None
    return render(request, 'login.html')


def dictfetchall(cursor):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        psw = request.POST['psw']
        user1 = users.objects.filter(username=username, password=psw)
        print(user1.count())
        if user1.count() > 0:
            request.session['username'] = username
            '''cursor=connection.cursor()
            #cursor.execute("select * from login_posts where username_id in (select f_username from login_friends where username_id=%s) or username_id=%s Order by upload_time desc",[username,username])
            cursor.execute("select login_users.image as u_img,login_posts.* from login_users,login_posts where username=username_id and username in (select f_username from login_friends where username_id=%s or f_username=%s) Order by upload_time desc",[username,username])
            posts = dictfetchall(cursor)
            cursor.execute("select * from login_users where username!=%s and username not in(select f_username from login_friends where username_id=%s)",[username,username])
            suggestion = dictfetchall(cursor)
            cursor.execute("select * from login_users where username=%s",[username])
            user123 = dictfetchall(cursor)
            return render(request,"home.html",{"posts":posts,"suggestion":suggestion,"name":user123})'''
            return redirect('home1')
        else:
            return render(request, "login.html", {"name": "Invalid password or username"})
    else:
        return redirect("/")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['dob']
        psw1 = request.POST['psw1']
        psw2 = request.POST['psw2']

        user1 = users.objects.filter(username=username)
        user2 = users.objects.filter(email=email)
        print(user1.count())
        print(user2.count())
        if user1.count() > 0:
            return render(request, "register.html", {"in": "Username is already taken"})
        elif user2.count() > 0:
            return render(request, "register.html", {"in": "Mail-id is already taken"})
        elif psw1 != psw2:
            return render(request, "register.html", {"in": "Password mismatch"})
        else:
            print("hello............................................")
            request.session['username'] = username
            user = users(username=username, password=psw1, name=name, email=email, phone_no=phone, dob=dob,
                         date_joined=date.today(), image="/media/default-profile-picture.jpg", otp=0, bio="")
            user.save()
            ######################### mail system ####################################
            sub = 'welcome to SNS'
            message = f"Your registration is successful.."
            email_from = settings.EMAIL_HOST_USER
            to = [email]
            send_mail(sub, message, email_from, to)
            return render(request, "uploadpic.html")
    else:
        return render(request, "register.html")


def forgot(request):
    if request.method == "POST":
        if(request.POST['otp']):
            name = request.POST['username']
            request.session['username'] = name
            user1 = users.objects.filter(username=name)
            print(user1.count())
            if user1.count() == 0:
                return render(request, "forgot.html", {"in": "Invlid username"})
            for i in user1:
                email = i.email
            digits = "0123456789"
            otp = ""
            for i in range(6):
                otp += digits[math.floor(random.random() * 10)]
            cursor = connection.cursor()
            cursor.execute(
                "Update login_users set otp=%s where username=%s", [otp, name])

            sub = 'OTP'
            message = f"OTP for password to reset is "+otp
            email_from = settings.EMAIL_HOST_USER
            to = [email]
            send_mail(sub, message, email_from, to)
            return render(request, "otp.html")
        else:  # need to write########################
            return render(request, "forgot.html", {"in": "Enter username"})
    else:
        return render(request, "forgot.html")


def otp(request):
    if request.session['username'] == None:
        return redirect('home')
    otp = request.POST['otp']
    name = request.session['username']
    user1 = users.objects.filter(username=name, otp=otp)
    print(user1.count())
    if user1.count() == 0:
        return render(request, "otp.html", {"in": "Invlid otp"})
    else:
        return render(request, "reset.html")


def reset(request):
    if request.session['username'] == None:
        return redirect('home')
    psw1 = request.POST['psw1']
    psw2 = request.POST['psw2']
    name = request.session['username']
    if psw1 != psw2:
        return render(request, "reset.html", {"in": "Password mismatch"})
    cursor = connection.cursor()
    cursor.execute(
        "Update login_users set password=%s where username=%s", [psw1, name])

    return render(request, "login.html", {"name": "Password reset successful.."})


def profile(request):
    if request.session['username'] == None:
        return redirect('home')
    if request.method == "POST":
        username = request.session['username']
        user_id = request.POST['user_id']
        request.session['friend'] = user_id
        request.session['p_id'] = user_id
        cursor = connection.cursor()
        cursor.execute(
            "select * from login_users where username=%s", [user_id])
        user123 = dictfetchall(cursor)
        cursor.execute(
            "select * from login_posts where username_id=%s Order by upload_time desc", [user_id])
        user321 = dictfetchall(cursor)
        cursor.execute(
            "select count(image_id) as c_i from login_posts where username_id=%s", [user_id])
        c_i = dictfetchall(cursor)
        cursor.execute(
            "select count(f_id) as c_f from login_friends where username_id=%s", [user_id])
        c_f = dictfetchall(cursor)
        cursor.execute(
            "select count(f_id) as c_u from login_friends where f_username=%s", [user_id])
        c_u = dictfetchall(cursor)
        user1 = friends.objects.filter(
            username_id=username, f_username=user_id)
        print(user1.count())
        if user1.count() > 0:
            d = 1
        else:
            d = 0
        return render(request, "profile.html", {"id": user123, "ac": user123, "posts": user321, "c_i": c_i, "c_f": c_f, "c_u": c_u, "d": d})
    # cursor=connection.cursor()
    #cursor.execute("select * from login_users where username=%s",[username])
    #user123 = dictfetchall(cursor)
    else:
        user_id = request.session['username']
        request.session['p_id'] = user_id
        cursor = connection.cursor()
        cursor.execute(
            "select * from login_users where username=%s", [user_id])
        user123 = dictfetchall(cursor)
        cursor.execute(
            "select * from login_posts where username_id=%s Order by upload_time desc", [user_id])
        user321 = dictfetchall(cursor)
        cursor.execute(
            "select count(image_id) as c_i from login_posts where username_id=%s", [user_id])
        c_i = dictfetchall(cursor)
        cursor.execute(
            "select count(f_id) as c_f from login_friends where username_id=%s", [user_id])
        c_f = dictfetchall(cursor)
        cursor.execute(
            "select count(f_id) as c_u from login_friends where f_username=%s", [user_id])
        c_u = dictfetchall(cursor)
        return render(request, "profile.html", {"id": user123, "posts": user321, "c_i": c_i, "c_f": c_f, "c_u": c_u, "d": 0})


def edit(request):
    if request.session['username'] == None:
        return redirect('home')
    if request.method == "POST":
        bio = request.POST['bio']
        cursor = connection.cursor()
        user_id = request.session['username']
        cursor.execute(
            "Update login_users set bio=%s where username=%s", [bio, user_id])
        cursor = connection.cursor()
        cursor.execute(
            "select * from login_users where username=%s", [user_id])
        user123 = dictfetchall(cursor)
        cursor.execute(
            "select * from login_posts where username_id=%s Order by upload_time desc", [user_id])
        user321 = dictfetchall(cursor)
        cursor.execute(
            "select count(image_id) as c_i from login_posts where username_id=%s", [user_id])
        c_i = dictfetchall(cursor)
        cursor.execute(
            "select count(f_id) as c_f from login_friends where username_id=%s", [user_id])
        c_f = dictfetchall(cursor)
        cursor.execute(
            "select count(f_id) as c_u from login_friends where f_username=%s", [user_id])
        c_u = dictfetchall(cursor)
        return render(request, "profile.html", {"id": user123, "posts": user321, "c_i": c_i, "c_f": c_f, "c_u": c_u, "d": 0})

    else:
        user_id = request.session['username']
        cursor = connection.cursor()
        cursor.execute(
            "select bio from login_users where username=%s", [user_id])
        user123 = dictfetchall(cursor)
        return render(request, "edit.html", {"user_id": user123})


def globe(request):
    if request.session['username'] == None:
        return redirect('home')
    cursor = connection.cursor()
    cursor.execute("select * from login_posts Order by upload_time desc")
    user123 = dictfetchall(cursor)
    return render(request, "global.html", {"pics": user123})


def logout(request):
    request.session['username'] = None
    logouts(request)
    # return render(request,"login.html")
    return redirect('home')


def simple_upload(request):
    if request.session['username'] == None:
        return redirect('home')
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        name = request.session['username']
        cursor = connection.cursor()
        cursor.execute("Update login_users set image=%s where username=%s", [
                       uploaded_file_url, name])
        return render(request, 'uploadpic.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'uploadpic.html')


def contin(request):
    request.session['username'] = None
    return render(request, 'login.html', {'name': "registration successful.."})


def add_friend(request):
    if request.session['username'] == None:
        return redirect('home')
    name = request.session['username']
    f_name = request.session['friend']
    user = friends(f_id=None, username_id=name, f_username=f_name)
    user.save()
    cursor = connection.cursor()
    cursor.execute(
        "select * from login_users where username not in (select f_username from login_friends where username_id =%s) and username !=%s", [name, name])
    suggestion = dictfetchall(cursor)
    return render(request, "friends.html", {"suggestion": suggestion})


def edit_dp(request):
    if request.session['username'] == None:
        return redirect('home')
    name = request.session['username']
    print(name)
    cursor = connection.cursor()
    cursor.execute("select * from login_users where username=%s", [name])
    uploaded_file_url = dictfetchall(cursor)
    print(uploaded_file_url)
    return render(request, 'editdp.html', {'uploaded_file_url': uploaded_file_url})
    # return render(request, 'uploadpic.html')


def contin2(request):
    if request.session['username'] == None:
        return redirect('home')
    user_id = request.session['username']
    cursor = connection.cursor()
    cursor.execute("select * from login_users where username=%s", [user_id])
    user123 = dictfetchall(cursor)
    cursor.execute(
        "select * from login_posts where username_id=%s Order by upload_time desc", [user_id])
    user321 = dictfetchall(cursor)
    cursor.execute(
        "select count(image_id) as c_i from login_posts where username_id=%s", [user_id])
    c_i = dictfetchall(cursor)
    cursor.execute(
        "select count(f_id) as c_f from login_friends where username_id=%s", [user_id])
    c_f = dictfetchall(cursor)
    cursor.execute(
        "select count(f_id) as c_u from login_friends where f_username=%s", [user_id])
    c_u = dictfetchall(cursor)
    return render(request, "profile.html", {"id": user123, "posts": user321, "c_i": c_i, "c_f": c_f, "c_u": c_u, "d": 0})


def edit_upload(request):
    if request.session['username'] == None:
        return redirect('home')
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url2 = fs.url(filename)
        name = request.session['username']
        cursor = connection.cursor()
        cursor.execute("Update login_users set image=%s where username=%s", [
                       uploaded_file_url2, name])
        return render(request, 'editdp.html', {'uploaded_file_url2': uploaded_file_url2})
    return render(request, 'editdp.html')


def addpostpic(request):
    if request.session['username'] == None:
        return redirect('home')
    if request.method == "POST":
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        if uploaded_file_url == "/media/city1.jpg":
            return render(request, 'addpostpic.html', {"error": "select a image"})
        upload_time = datetime.now()
        name = request.session['username']
        user = posts(image_id=None, upload_time=upload_time,
                     des="", username_id=name, image=uploaded_file_url)
        user.save()
        user1 = posts.objects.filter(upload_time=upload_time)
        for i in user1:
            request.session['img_id'] = i.image_id
        print(request.session['img_id'])
        return render(request, 'addpostpic.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'addpostpic.html')


def addpost(request):
    if request.session['username'] == None:
        return redirect('home')
    if request.method == "POST":
        desc = request.POST["desc"]
        cursor = connection.cursor()
        cursor.execute("Update login_posts set des=%s where image_id=%s", [
                       desc, request.session['img_id']])
        '''username=request.session['username']
        cursor=connection.cursor()
        #cursor.execute("select * from login_posts where username_id in (select f_username from login_friends where username_id=%s) or username_id=%s Order by upload_time desc",[username,username])
        cursor.execute("select login_users.image as u_img,login_posts.* from login_users,login_posts where username=username_id and username in (select f_username from login_friends where username_id=%s or f_username=%s) Order by upload_time desc",[username,username])
        posts = dictfetchall(cursor)
        cursor.execute("select * from login_users where username!=%s and username not in(select f_username from login_friends where username_id=%s)",[username,username])
        suggestion = dictfetchall(cursor)
        cursor.execute("select * from login_users where username=%s ",[username])            
        user123 = dictfetchall(cursor)
        return render(request,"home.html",{"posts":posts,"suggestion":suggestion,"name":user123})'''
        return redirect('home1')

    return render(request, 'addpost.html')


def friend(request):
    if request.session['username'] == None:
        return redirect('home')
    username = request.session['username']
    cursor = connection.cursor()
    cursor.execute(
        "select * from login_users where username not in (select f_username from login_friends where username_id=%s) and username!=%s", [username, username])
    suggestion = dictfetchall(cursor)
    return render(request, "friends.html", {"suggestion": suggestion})


def chatbox(request):
    if request.session['username'] == None:
        return redirect('home')
    if request.method == 'POST':
        sub = 'Message from ' + request.session['username']
        message = f""+request.POST['mess']
        email_from = settings.EMAIL_HOST_USER
        user1 = users.objects.filter(username=request.session['friend'])
        for i in user1:
            email = i.email
        to = [email]
        send_mail(sub, message, email_from, to)
        print(request.POST['mess'])
        return render(request, "chat1.html", {"to_id": request.session['friend'], "note": "Message Sent..."})
    return render(request, "chat1.html", {"to_id": request.session['p_id']})


def follow_g(request):
    if request.session['username'] == None:
        return redirect('home')
    username = request.session['p_id']
    cursor = connection.cursor()
    cursor.execute(
        "select * from login_users where username in (select f_username from login_friends where username_id=%s)", [username])
    suggestion = dictfetchall(cursor)
    l_s = len(suggestion)
    return render(request, "following.html", {"suggestion": suggestion, "l_s": l_s})


def follow_r(request):
    if request.session['username'] == None:
        return redirect('home')
    username = request.session['p_id']
    cursor = connection.cursor()
    cursor.execute(
        "select * from login_users where username in (select username_id from login_friends where f_username=%s)", [username])
    suggestion = dictfetchall(cursor)
    l_s = len(suggestion)
    return render(request, "followers.html", {"suggestion": suggestion, "l_s": l_s})


def home1(request):
    if request.session['username'] == None:
        return redirect('home')
    username = request.session['username']
    cursor = connection.cursor()
    #cursor.execute("select * from login_posts where username_id in (select f_username from login_friends where username_id=%s) or username_id=%s Order by upload_time desc",[username,username])
    cursor.execute(
        "select login_users.image as u_img,login_posts.* from login_users,login_posts where username=username_id and username in (select f_username from login_friends where username_id=%s or f_username=%s) Order by upload_time desc", [username, username])
    posts = dictfetchall(cursor)
    cursor.execute(
        "select * from login_users where username!=%s and username not in(select f_username from login_friends where username_id=%s)", [username, username])
    suggestion = dictfetchall(cursor)
    cursor.execute("select * from login_users where username=%s ", [username])
    user123 = dictfetchall(cursor)

    return render(request, "home.html", {"posts": posts, "suggestion": suggestion, "name": user123})
