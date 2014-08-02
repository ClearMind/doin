# -*- coding: utf-8 -*-
import os

from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from attestation.models import *
from lxml import html
from libs.ODTFile import ODTFile
from settings import MEDIA_ROOT

class TestURLs(TestCase):
    fixtures = ['attestation/fixtures/test_data.json']

    def setUp(self):
        user = User.objects.create(username='admin')
        user.set_password('325756')
        user.save()
        self.c = Client()
        self.c.login(username='admin', password='325756')

    def test_urls(self):
        c = Client()
        self.assertEquals(c.get(reverse('attestation.views.request_form')).status_code, 200)
        self.assertEquals(c.get(reverse('config.views.index')).status_code, 200)
        self.assertEquals(c.get(reverse('django.contrib.auth.views.login')).status_code, 200)

    def test_auth_urls(self):
        self.assertEquals(self.c.get(reverse('attestation.views.requests')).status_code, 200)
        response = self.c.post(reverse('django.contrib.auth.views.login'),data={'username': 'admin', 'password': '325756',
                                                                           'next': "/"})
        self.assertRedirects(response, '/')

    def test_requests(self):
        self.assertEquals(Request.objects.count(), 2)
        rs = Request.objects.all()
        r = rs[0]
        self.assertHTMLEqual(u'%s' % self.c.get(reverse('attestation.views.request_by_id', args=[r.pk])).content.decode('utf-8'),
                             u'%s' % self.c.get(reverse('attestation.views.request', args=[r.secret_code])).content.decode('utf-8'))


class TestForms(TestCase):
    fixtures = ['attestation/fixtures/test_data.json']

    def setUp(self):
        self.c = Client()

    def test_request_form(self):
        data = {
            'first_name': u'Алекснадр',
            'last_name': u'Южаков',
            'middle_name': u'Сергеевич',
            'genitive': u'Южакова Александра Сергеевича',
            'birth_date': '2012-11-09',
            'post_date': '2012-11-09',
            'email': 'tech@surgpu.ru',
            'phone': '',
            'discipline': 'ddd355',
            'post': 1,
            'territory': 21,
            'organization': '',
            'organization_name': 'СурГПУ',
            'with_qualification': '',
            'expiration_date': '',
            'organization_experience': 5,
            'post_experience': 5,
            'edu_institution': 'СурГПУ',
            'edu_speciality': 'Математика',
            'edu_qualification': 'Математика',
            'edu_diploma_year': 2007,
            'edu_institution2': '',
            'edu_speciality2': '',
            'edu_qualification2': '',
            'edu_diploma_year2': '',
            'degrees': [],
            'academic_title': '',
            'achievements': [],
            'qualification': 2,
            'presence': '',
            'experience': 7,
            'ped_experience': 5,
            'trainings': '',
            'results': 'My mega results'
        }
        response = self.c.post(reverse('attestation.views.request_form'), data=data)
        print response.content
        r = Request.objects.order_by("-id")[0]
        self.assertRedirects(response, reverse('attestation.views.request',
            args=[r.secret_code]))
        self.assertEquals(r.discipline, 'ddd355')


class TestExpertSheet(TestCase):
    fixtures = ['attestation/fixtures/test_data.json']

    def setUp(self):
        self.c = Client()

        self.r = Request.objects.all()[0]
        self.eir = ExpertInRequest.objects.filter(request=self.r)[0]

    def test_url(self):

        # must can get url /attestation/expert_sheet/(rcode)/(expert_id)/
        resp = self.c.get(reverse("attestation.views.expert_sheet", args=[self.r.secret_code, self.eir.pk]))
        self.assertEquals(resp.status_code, 200)

    def test_content(self):
        resp = self.c.get(reverse("attestation.views.expert_sheet", args=[self.r.secret_code, self.eir.pk]))
        content = resp.content
        h = html.fromstring(content)
        expert_name_el = h.cssselect('#expert-name')
        assert len(expert_name_el) > 0


class TestODFGenerator(TestCase):

    def test_open_file(self):
        """
        Должна быть возможность открывать файлы типа ODT для их последующего использования
        """
        file = ODTFile(os.path.join(MEDIA_ROOT, "odt/protocol.odt"))
        copy_path = os.path.join(MEDIA_ROOT, "odt/protocol_copy.odt")
        file.save(copy_path)

        assert os.path.exists(copy_path)
        os.remove(copy_path)

    def test_text_replace(self):
        """

        """
        pass

