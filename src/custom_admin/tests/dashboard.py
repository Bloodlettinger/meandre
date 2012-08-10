# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_webtest import WebTest

from ... test_settings import *


class BasicTest(WebTest):

    def setUp(self):
        self.admin = User.objects.create_superuser(Test.ADMIN_LOGIN, Test.ADMIN_EMAIL, Test.ADMIN_PASS)

        form = self.app.get(reverse('admin:index')).form
        form['username'] = Test.ADMIN_LOGIN
        form['password'] = Test.ADMIN_PASS
        self.assertRedirects(form.submit(), reverse('admin:index'))
        self.app.get(reverse('admin:storage_project_changelist'))

    def test_app_index(self):
        url = reverse('admin:app_list', args=('storage', ))
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
