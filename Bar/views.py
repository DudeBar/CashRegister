from Bar.form import OpenForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from Bar.models import BarMan, Category


def home(request):
    if request.user.is_authenticated():
        barmans = BarMan.objects.all()
        return render(request, "opened_home.html", {
            'barmans': barmans
        })
    else:
        return render(request, "closed_home.html", {})

def open(request):
    if request.method == "POST":
        form = OpenForm(request.POST)
        if form.is_valid():
            session = "session"
            password = form.cleaned_data['password']
            user = authenticate(username=session, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("home")
                else:
                    return redirect("open")
            else:
                return redirect("open")
        else:
            return render(request, "open.html", {'form':form})
    else:
        form = OpenForm()
        return render(request, "open.html", {'form':form})

def close(request):
    logout(request)
    return redirect("home")

def make_command(self, barman_id):
    categories = Category.objects.filter(parent=None)
    print categories