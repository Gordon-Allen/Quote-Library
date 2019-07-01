from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = ('Invalid Email Address')
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Passwords do not match"
        if len(postData['date_of_birth']) < 4:
            errors["date_of_birth"] = "Date of Birth required"

        return errors

    def login_validator(self, postData):
        user = User.objects.filter(email=postData['login_email'])
        errors = {}
        if not user:
            errors['email'] = "Please enter a valid email address"
        if user and not bcrypt.checkpw(postData['login_password'].encode('utf8'), user[0].password.encode('utf8')):
            errors['password'] = "Incorrect Password"
        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['quoted_by']) < 3:
            errors["quoted_by"] = "Quotes by should be at least 3 characters"
        if len(postData['message']) < 10:
            errors["message"] = "Message should be at least 10 characters"
        return errors

    def add_favorite_user(self, user_id, quote_id):
        quote = Quote.objects.get(id=quote_id)
        current_user = User.objects.get(id=user_id)
        quote.favorited_user.add(current_user)

    def remove_favorite(self, user_id, quote_id):
        quote = Quote.objects.get(id=quote_id)
        current_user = User.objects.get(id=user_id)
        quote.favorited_user.remove(current_user)

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    date_of_birth= models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 

class Quote(models.Model):
    quoted_by = models.CharField(max_length=100)
    message = models.TextField()
    author = models.ForeignKey(User, related_name='posted_quotes')
    favorited_user = models.ManyToManyField(User, related_name='favorited_quote')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager() 

