from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
import datetime
from .models import *

def index(request):
    if "id" in request.session.keys():
        redirect('/quotes')
    return render(request, 'q_library_app/index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        date_of_birth = request.POST['date_of_birth']
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed_password, date_of_birth=date_of_birth)
        user.save()
        request.session['id'] = user.id 
        return redirect("/quotes")

def quotes(request):
    all_users= User.objects.all()
    current_user = User.objects.get(id=request.session['id'])
    favorites = Quote.objects.filter(favorited_user=request.session['id'])
    all_quotes = Quote.objects.all().exclude(favorited_user=request.session['id'])
    context = {
        "all_users" : all_users,
        "current_user" : current_user,
        "all_quotes" : all_quotes,
        "favorites" : favorites,
    }
    return render(request, 'q_library_app/quotes.html', context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        user = User.objects.get(email=request.POST['login_email'])
        request.session['id'] = user.id
        return redirect('/quotes')

def log_out(request):
    del request.session['id']
    return redirect('/')

def add_quote(request):
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        Quote.objects.create(quoted_by=request.POST['quoted_by'], message=request.POST['message'], author=User.objects.get(id=request.session['id']))
        return redirect('/quotes')

def view_user (request, user_id):
    author = User.objects.get(id=user_id)
    current_user = User.objects.get(id=request.session['id'])
    context = {
        "quotes" : Quote.objects.filter(author=author),
        "author" : author,
        "current_user" : current_user,
    }
    return render (request, "q_library_app/users.html", context)

def add_favorite(request, quote_id):
    user_id = request.session['id']
    Quote.objects.add_favorite_user(user_id, quote_id)
    return redirect('/quotes')

def remove_favorite(request, quote_id):
    user_id = request.session['id']
    Quote.objects.remove_favorite(user_id, quote_id)
    return redirect('/quotes')
