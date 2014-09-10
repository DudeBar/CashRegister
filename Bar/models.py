from django.db import models

class BarMan(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey("self",null=True, blank=True, default=None)

    @classmethod
    def get_category_path(self, category, path = []):
        if category.parent:
            path.append(category.parent)
            self.get_category_path(category.parent, path)
        return path

    def __unicode__(self):
        return self.name

class Session(models.Model):
    start_session = models.DateTimeField()
    end_session = models.DateTimeField(null=True)
    total_money = models.FloatField(default=0)
    en_cours = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    stock = models.IntegerField()
    alert_stock = models.IntegerField()
    price = models.FloatField()
    happy_hour = models.FloatField()
    tva = models.FloatField()

    def __unicode__(self):
        return self.name

class Commande(models.Model):
    payment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
    barman = models.ForeignKey(BarMan)
    session = models.ForeignKey(Session)
    total_price = models.FloatField()

class Commande_has_products(models.Model):
    commande = models.ForeignKey(Commande)
    product = models.ForeignKey(Product)
    price = models.FloatField()

class Config(models.Model):
    variable = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

