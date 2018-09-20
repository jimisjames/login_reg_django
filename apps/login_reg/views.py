from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):

    return render(request, "login_reg/index.html")


def success(request, id):
    user = User.objects.get(id=id)
    context = {
        "user" : user
    }
    request.session.clear()
    return render(request, "login_reg/success.html", context)


def reg(request):

    errors = User.objects.validate(request.POST)

    if len(errors):
        for key, val in errors.items():
            messages.info(request, val, extra_tags=key)
            request.session["first_name"] = request.POST["first_name"]
            request.session["last_name"] = request.POST["last_name"]
            request.session["email"] = request.POST["email"]
        return redirect("/")    # failure
    else:
        hashed_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=hashed_pw)
        print(new_user)

        return redirect("/success/%s" % new_user.id)    # success


def login(request):

    result = User.objects.login(request.POST)
    errors = result[0]
    print(result)
    user_id = result[1]

    if len(errors):
        for val in errors:
            messages.warning(request, val)
            request.session["email2"] = request.POST["email"]
        return redirect("/")    # failure
    else:
        return redirect("/success/%s" % user_id)    # success