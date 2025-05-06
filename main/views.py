from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Car

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def profile_view(request):
    searchQ = request.GET.get('search', '').strip()

    if searchQ:
        owned_cars = Car.objects.filter(
            owner=request.user,
            list_type='owned',
            name__icontains=searchQ
        )
    else:
        owned_cars = Car.objects.filter(owner=request.user, list_type='owned')

    wanted_cars = Car.objects.filter(owner=request.user, list_type='wanted')
    
    return render(request, 'main/profile.html', {
        'owned_cars': owned_cars,
        'wanted_cars': wanted_cars,
    })

def add_car(request):
    if request.method == 'POST':
        car_name = request.POST.get('car_name')
        list_type = request.POST.get('list_type')
        if car_name and list_type in ['owned', 'wanted']:
            Car.objects.create(name=car_name, owner=request.user, list_type=list_type)
    return redirect('profile')

def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)
    car.delete()
    return redirect('profile')

def move_car_to_owned(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user, list_type='wanted')
    car.list_type = 'owned'
    car.save()
    return redirect('profile')

def logout_view(request):
    logout(request)
    return redirect('home')