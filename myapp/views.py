from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message, Topic
from .forms import RoomForm
from User_auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import  login_required
from .forms import RoomForm, UserForm


def loginPage(request):
    page ='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try: 
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Login Failed: User not found')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')

    context = {'page':page}
    return render(request, 'myapp/login_register.html', context)




def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect ('home')
    page ='register'
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect ('home')

        else:
            messages.error(request," An error occurred during registration")
    context = {'page':page,'form':form}
    return render(request,'myapp/login_register.html', context)

def home(request):
    q = request.GET.get('q') 
    if q != None:
        pass
    else:
        q = ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    all_topics = Topic.objects.all()
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 'topics':topics,
     'room_count':room_count, 'room_messages':room_messages,'all_topics':all_topics}
    return render(request, 'myapp/home.html',context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":
        body = request.POST.get('body')
        user = request.user
        room = room
        
        Message.objects.create(user=user,body=body,room=room)
        
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {'room':room,"room_messages":room_messages,"participants":participants}

    return render(request, 'myapp/room.html', context)

def profilePage(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user_':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request, 'myapp/profile.html', context)

@login_required(login_url='login')
def editUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)

    return render(request, 'myapp/edit-user.html', {'form': form})

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'myapp/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'myapp/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room= Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not permitted for this action!")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'myapp/delete.html',{'obj':room})
# Create your views here.
        





@login_required(login_url='/login')
def deleteMessage(request, pk, sd):
    message= Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("You are not permitted for this action!")
    if request.method == 'POST':
        message.delete()
        if sd == 'home':
            return redirect('home')
        else:
            return redirect('room', sd)
            #return redirect(request.META.get('HTTP_REFERER'))
        #except:
         #   return redirect('room', sd)
        #return redirect('home')
    return render(request, 'myapp/delete.html',{'obj':message})

 
def topicsPage(request):
    q = request.GET.get('q') 
    if q != None:
        pass
    else:
        q = ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'myapp/topics.html', {'topics':topics})


def activityPage(request):
    room_messges = Message.objects.all()
    return render(request,'myapp/activity.html',{'room_messges':room_messges})