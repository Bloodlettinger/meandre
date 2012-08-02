# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_webtest import WebTest

from .. models import Customer
from . settings import *

__all__ = ('ProjectTest', )


class ProjectTest(WebTest):

    def setUp(self):
        self.admin = User.objects.create_superuser(ADMIN_LOGIN, ADMIN_EMAIL, ADMIN_PASS)
        self.customer = Customer.objects.create(
            customer_type=1,
            partnership_type=1,
            code='0000',
            short_name='customer'
            )
        form = self.app.get(reverse('admin:index')).form
        form['username'] = ADMIN_LOGIN
        form['password'] = ADMIN_PASS
        self.assertRedirects(form.submit(), reverse('admin:index'))
        self.app.get(reverse('admin:storage_project_changelist'))

    def test_create(self):
        url = reverse('admin:storage_project_add')
        form = self.app.get(url).forms['project_form']
        form['customer'] = self.customer.pk
        form['short_name_ru'] = u'тест'
        form['short_name_en'] = u'test'
        self.assertRedirects(form.submit(), reverse('admin:storage_project_changelist'))
