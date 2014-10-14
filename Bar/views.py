import json
from Bar.form import OpenForm, NoteForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from Bar.models import BarMan, Category, Product, Commande, Session, Commande_has_products, Note
from Bar.tasks import send_fidelity
from django.db.models import Count, Avg, Sum


def home(request):
    notes_list = Note.objects.all().order_by('-pk')
    if request.user.is_authenticated():
        happy_hour=False
        if "happy_hour" not in request.session.keys():
            request.session["happy_hour"]=False
        else:
            happy_hour=request.session.get("happy_hour")

        barmans = BarMan.objects.all()
        last_commands = Commande.objects.all().order_by('-date')[:10]
        return render(request, "opened_home.html", {
            'happy_hour': happy_hour,
            'barmans': barmans,
            'last_commands': last_commands,
            'notes': notes_list
        })
    else:
        if Session.objects.filter(en_cours=1).exists():
            session = Session.objects.get(en_cours=1)
            session.en_cours=0
            session.save()
        return render(request, "closed_home.html", {'notes': notes_list})

@login_required
def set_happy_hour(request):
    if request.session.get("happy_hour"):
        request.session["happy_hour"]=False
    else:
        request.session["happy_hour"]=True
    return redirect("home")

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
                    if "happy_hour" not in request.session.keys():
                        request.session["happy_hour"]=False
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
    try:
        session = Session.objects.get(en_cours=1)
        session.en_cours = 0
        session.save()
    except:
        pass
    logout(request)
    return redirect("home")

@login_required
def make_command(request, barman_id):
    categories = Category.objects.filter(parent=None).order_by('name')
    current_session = Session.objects.get(en_cours=1)
    best_product_list = Commande_has_products.objects.values('product').annotate(pcount=Count('product')).order_by('-pcount')[:3]
    day_best_product_list = Commande_has_products.objects.filter(commande__session=current_session).values('product').annotate(pcount=Count('product')).order_by('-pcount')[:3]
    products = []
    for product in best_product_list:
        product_objects = Product.objects.get(pk=product['product'])
        products.append(product_objects)
    for product in day_best_product_list:
        product_objects = Product.objects.get(pk=product['product'])
        if product_objects not in products:
            products.append(product_objects)

    return render(request, "make_command.html", {
                        "barman_id":barman_id,
                        "categories":categories,
                        "products": products,
                        "happy_hour":request.session["happy_hour"]
    })

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
        products = Product.objects.filter(category=category).order_by('name')
        for product in products:
            json_products.append({product.pk:product.name})
        if category_id != 0:
            child_categories = Category.objects.filter(parent=category).order_by('name')
        else:
            child_categories = Category.objects.filter(parent=None).order_by('name')
        for child in child_categories:
            json_categories.append({child.pk:child.name})
        return HttpResponse(json.dumps({"path":json_path, "products":json_products, "categories":json_categories}))
    else:
        return redirect("home")

@login_required
def product_onclick(request, product_id):
    if request.is_ajax():
        product = Product.objects.get(pk=product_id)
        return HttpResponse(json.dumps({"id":product.pk, "name":product.name, "price":product.price, "happy_hour":product.happy_hour}))
    else:
        return redirect('home')

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
            session.total_money += float(total_price)
            session.save()
            send_fidelity.delay(product_list)
            return HttpResponse(json.dumps({"result" : True, "data" : "OK" }), content_type="application/json")
        except:
            return HttpResponse(json.dumps({"result" : True, "data" : "NOK" }), content_type="application/json")
    else:
        raise Http404

@login_required
def get_solde(request):
    if request.is_ajax():
        commandes = Commande.objects.filter(session__en_cours=1).aggregate(total=Sum('total_price'))
        nb_commandes = Commande.objects.filter(session__en_cours=1).count()
        return HttpResponse(json.dumps({"total" : commandes['total'], "nb_command": nb_commandes}), content_type="application/json")
    else:
        raise Http404

@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            Note.objects.create(title=form.cleaned_data['title'], text=form.cleaned_data['text'], type=form.cleaned_data['type'])
            return redirect("home")
        else:
            return render(request, "add_note.html", {'form': form})
    else:
        form = NoteForm()
        return render(request, "add_note.html", {'form': form})

@login_required
def del_note(request):
    if request.is_ajax():
        note_id = request.POST['note_id']
        note = Note.objects.get(pk=note_id)
        note.delete()
        return HttpResponse(json.dumps({"result" : True, "data" : "OK" }), content_type="application/json")
    else:
        return redirect("home")