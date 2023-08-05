from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Registration,Room, Message
from django.http import HttpResponse, JsonResponse
from readmission.need_to_revisit import get_id
from datetime import date, timedelta


# Create your views here.
def home(request):
    if(request.user.is_anonymous):
        return render(request, 'readmission/home.html')
    elif(request.user.is_superuser):
        return redirect('logout')
    else:
        data = Registration.objects.filter(username=request.user)
        return render(request, 'readmission/home.html',{'userdetails':data[0]})

def services(request):
    today = date.today()
    after_date = today + timedelta(days=60) #>30
    before_date = today + timedelta(days=30) #<30

    if request.method == 'POST':
        encounter_id = request.POST['encounter_id']
        print(type(encounter_id))
        result = get_id(int(encounter_id))
        if(result.values[0] == '>30'):
            result.values[0] = 'You should be admitted between '+str(before_date)+' and '+str(after_date)
        elif(result.values[0] == '<30'):
            result.values[0] = 'You should be admitted before '+str(before_date)+' in the hospital'
        else:
            result.values[0] = 'You need not be admitted in a hospital'
        print(result)
        return render(request,"readmission/services.html",{'status':'1','result':result.values[0]})
    else:
        return render(request, "readmission/services.html",{'status':'0'})


def livechat(request):
    return render(request, 'readmission/livechat.html')


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'readmission/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/' + room + '/?username=' + username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/' + room + '/?username=' + username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})



def register(request):
    if (request.method == 'POST'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if (password1 == password2):
            if (User.objects.filter(username=username).exists()):
                messages.warning(request, "Username already taken")
                return redirect('/register')
            elif (User.objects.filter(email=email).exists()):
                messages.warning(request, "Email already taken")
                return redirect('/register')
            elif (Registration.objects.filter(mobile=mobile).exists()):
                messages.warning(request, "Mobile number already taken")
                return redirect('/register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1,
                                                first_name=first_name, last_name=last_name)
                New_user = Registration(first_name=first_name, last_name=last_name, username=username, email=email,
                                        password=password1, mobile=mobile)
                New_user.save()
                user.save()
                messages.success(request, "Your account has been created successfully")
        else:
            messages.warning(request, "Passwords not matching")
            return redirect('/register')

        return redirect('/login')
    else:
        return render(request, "readmission/register.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #    print(username)
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.warning(request, 'Invalid credentials')
            return redirect('/login')
    else:
        return render(request, "readmission/login.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def dashboard(request):
    data = Registration.objects.filter(username=request.user)
    return render(request, "readmission/dashboard.html",{'userdetails':data[0]})



