from django.core import mail
from django.test import TestCase
from portifolio.contatos.forms import Contato

class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/contato/')

    def test_get(self):
        """deve retornar status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """tem que ter um template"""
        self.assertTemplateUsed(self.resp, 'contatos/contato.html')

    def test_html(self):
        """tem que ter tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 4)
        self.assertContains(self.resp, 'type="text"', 2)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """teste sem nome 1"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """teste sem nome 2"""
        form = self.resp.context['form']
        self.assertIsInstance(form, Contato)

    def test_form_has_fields(self):
        """form tem que ter 4 campos"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'email', 'phone', 'message'], list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Vinicius Damaceno',
                    email='contato@viniciusdamaceno.com.br',
                    phone='91980869474',
                    message='preciso de um orçamento')
        self.resp = self.client.post('/contato/', data)

    def test_post(self):
        """redireciona pro contato"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_contato_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_contato_email_subject(self):
        email = mail.outbox[0]
        expect = 'Contato feito pelo site'

        self.assertEqual(expect, email.subject)

    def test_contato_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@viniciusdamaceno.com.br'

        self.assertEqual(expect, email.from_email)

    def test_contato_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@viniciusdamaceno.com.br']

        self.assertEqual(expect, email.to)

    def test_contato_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Vinicius Damaceno', email.body)
        self.assertIn('contato@viniciusdamaceno.com.br', email.body)
        self.assertIn('91980869474', email.body)
        self.assertIn('preciso de um orçamento', email.body)

class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/contato/', {})

    def test_post(self):
        """dados invalidos nao enviam"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'contatos/contato.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, Contato)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class ContatoSucessMessage(TestCase):
    def test_message(self):
        data = dict(name='Vinicius Damaceno',
                    email='contato@viniciusdamaceno.com.br',
                    phone='91980869474',
                    message='preciso de um orçamento')

        response = self.client.post('/contato/', data, follow=True)
        self.assertContains(response, 'Mensagem enviada com sucesso!')