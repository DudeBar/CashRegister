from django.test import TestCase
from Bar.models import BarMan, Note, Commande, Commande_has_products


class CashTestCase(TestCase):

    fixtures = ['users_fixture.json']

    def login(self):
        response = self.client.post("/open",{'password':'1212'})
        return response

class AccesTestCase(CashTestCase):

    def test_open_cashregister(self):
        response = self.client.post("/open",{'password':'1212'})
        self.assertRedirects(response,'/',302)

    def test_open_wrong_password_cashregister(self):
        response = self.client.post("/open",{'password':'pouet'})
        self.assertRedirects(response,'/open',302)

class HomeTestCase(CashTestCase):

    def setUp(self):
        self.barman = BarMan.objects.create(name='dude-barman')

    def test_home_barman_list(self):
        self.login()
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response,'/make_command/'+str(self.barman.pk)+'/')
        self.assertContains(response, self.barman.name)

    def test_home_add_note(self):
        self.login()
        response = self.client.post('/add_note/', {'title': 'la note', 'text':'texte de note', 'type':1})
        self.assertRedirects(response, '/', 302)
        notes = Note.objects.all()
        self.assertEquals(notes[0].title, 'la note')
        self.assertEquals(notes[0].text, 'texte de note')

    def test_home_del_note(self):
        self.login()
        note = Note.objects.create(title="le titre", text="le texte", type=1)
        note_id = note.pk
        nb_notes = Note.objects.all().count()
        self.assertEquals(nb_notes, 1)
        self.client.post('/del_note/', {'note_id': note_id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        nb_notes = Note.objects.all().count()
        self.assertEquals(nb_notes, 0)

    def test_home_add_note_without_right(self):
        response = self.client.post('/add_note/', {'title': 'la note', 'text':'texte de note', 'type':1})
        self.assertRedirects(response, '/open?next=/add_note/', 302)

    def test_activate_happy_hour(self):
        self.login()
        response = self.client.get('/set_happy_hour/')
        self.assertRedirects(response, '/', 302)
        self.assertEquals(self.client.session["happy_hour"], True)
        self.client.get('/set_happy_hour/')
        self.assertEquals(self.client.session["happy_hour"], False)

class CommandTestCase(CashTestCase):

    fixtures = ['users_fixture.json', 'products_fixture.json', 'category_fixture.json']

    def setUp(self):
        self.barman = BarMan.objects.create(name='dude-barman')

    def test_access_command_page(self):
        self.login()
        response = self.client.get('/make_command/'+str(self.barman.pk)+'/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['categories']), 9)

    def test_categories_navigation(self):
        self.login()
        response = self.client.get('/category_onclick/5/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert_response = '{"path": [{"1": "Bi\u00e8res"}, {"0": "Racine"}], "products": [{"1": "Demi Estaminet"}, {"3": "Demi Karmelite"}, {"53": "Demi Picon"}, {"8": "Demi Wit"}, {"5": "Palm Royale"}, {"7": "Steenbrugge Brune"}], "categories": []}'
        self.assertEquals(response.content, assert_response)

    def test_categories_navigation_without_login(self):
        response = self.client.get('/category_onclick/5/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertRedirects(response, '/open?next=/category_onclick/5/', 302)

    def test_categories_navigation_without_ajax(self):
        self.login()
        response = self.client.get('/category_onclick/5/')
        self.assertRedirects(response, '/', 302)

    def test_add_product_to_command(self):
        self.login()
        response = self.client.get('/product_onclick/12/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert_response = '{"price": 5.0, "id": 12, "happy_hour": 5.0, "name": "Verre Vinojito"}'
        self.assertEquals(response.content, assert_response)

    def test_add_product_without_login(self):
        response = self.client.get('/product_onclick/12/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertRedirects(response, '/open?next=/product_onclick/12/', 302)

    def test_add_product_without_ajax(self):
        self.login()
        response = self.client.get('/product_onclick/12/')
        self.assertRedirects(response, '/', 302)

    def test_add_command(self):
        self.login()
        response = self.client.post(
            '/add_command/',
            {
                'barman': self.barman.pk,
                'total_price':12.5,
                'product_list':'[{"price": 5.0, "id": 12, "happy_hour": 5.0, "name": "Verre Vinojito"}]'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '{"data": "OK", "result": true}')
        command = Commande.objects.all()
        self.assertEquals(len(command), 1)
        self.assertEquals(command[0].total_price, 12.5)
        command_products = Commande_has_products.objects.filter(commande = command)
        self.assertEquals(len(command_products), 1)
        self.assertEquals(command_products[0].price, 5.0)

    def test_add_command_without_login(self):
        response = self.client.post(
            '/add_command/',
            {
                'barman': self.barman.pk,
                'total_price':12.5,
                'product_list':'[{"price": 5.0, "id": 12, "happy_hour": 5.0, "name": "Verre Vinojito"}]'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertRedirects(response, '/open?next=/add_command/', 302)

    def test_add_command_without_ajax(self):
        self.login()
        response = self.client.post(
            '/add_command/',
            {
                'barman': self.barman.pk,
                'total_price':12.5,
                'product_list':'[{"price": 5.0, "id": 12, "happy_hour": 5.0, "name": "Verre Vinojito"}]'
            }
        )
        self.assertEquals(response.status_code, 404)

    def test_add_command_without_get(self):
        self.login()
        response = self.client.get(
            '/add_command/',
            {
                'barman': self.barman.pk,
                'total_price':12.5,
                'product_list':'[{"price": 5.0, "id": 12, "happy_hour": 5.0, "name": "Verre Vinojito"}]'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 404)