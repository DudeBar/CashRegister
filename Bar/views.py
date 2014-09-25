import json
from Bar.form import OpenForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from Bar.models import BarMan, Category, Product, Commande, Session, Commande_has_products
from Bar.tasks import send_fidelity


def home(request):
    if request.user.is_authenticated():
        barmans = BarMan.objects.all()
        last_commands = Commande.objects.all().order_by('-date')[:10]
        return render(request, "opened_home.html", {
            'barmans': barmans,
            'last_commands': last_commands
        })
    else:
        if Session.objects.filter(en_cours=1).exists():
            session = Session.objects.get(en_cours=1)
            session.en_cours=0
            session.save()
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
                    Session.objects.create(en_cours=1)
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
    session = Session.objects.get(en_cours=1)
    session.en_cours = 0
    session.save()
    logout(request)
    return redirect("home")

@login_required
def make_command(request, barman_id):
    categories = Category.objects.filter(parent=None)
    return render(request, "make_command.html", {"barman_id":barman_id, "categories":categories})

def _get_category_path(category, path = []):
    category = Category.objects.get(pk=category)
    if category.parent:
        path.append(category.parent.pk)
        _get_category_path(category.parent.pk, path)
    return path

@login_required
def category_onclick(request, category_id):
    if request.is_ajax():
        if Category.objects.filter(pk=category_id).exists():
            category = Category.objects.get(pk=category_id)
            category_path = Category.get_category_path(category,[])
        else:
            category = None
            category_path = []
        json_path = []
        json_products = []
        json_categories = []
        for path in category_path:
            json_path.append({path.pk:path.name})
        json_path.append({0:"Racine"})
        products = Product.objects.filter(category=category)
        for product in products:
            json_products.append({product.pk:product.name})
        if category_id != 0:
            child_categories = Category.objects.filter(parent=category)
        else:
            child_categories = Category.objects.filter(parent=None)
        for child in child_categories:
            json_categories.append({child.pk:child.name})
        return HttpResponse(json.dumps({"path":json_path, "products":json_products, "categories":json_categories}))

@login_required
def product_onclick(request, product_id):
    if request.is_ajax():
        product = Product.objects.get(pk=product_id)
        return HttpResponse(json.dumps({"id":product.pk, "name":product.name, "price":product.price, "happy_hour":product.happy_hour}))

@login_required
def add_command(request):
    if request.method == "POST" and request.is_ajax():
        try:
            session = Session.objects.get(en_cours=1)
            product_list = json.loads(request.POST.get("product_list"))
            barman_id = request.POST.get("barman")
            barman = BarMan.objects.get(pk=barman_id)
            total_price = request.POST.get("total_price")
            command = Commande(barman=barman, total_price=total_price, payment="Espece", session=session)
            command.save()
            for product_command in product_list:
                product = Product.objects.get(pk=product_command['id'])
                Commande_has_products.objects.create(commande=command, product=product, price=product_command["price"])
            send_fidelity.delay()
            return HttpResponse(json.dumps({"result" : True, "data" : "OK" }), content_type="application/json")
        except:
            return HttpResponse(json.dumps({"result" : True, "data" : "NOK" }), content_type="application/json")

