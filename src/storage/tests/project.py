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
        self.customer2 = Customer.objects.create(
            customer_type=2,
            partnership_type=2,
            code='0001',
            short_name='customer2'
            )
        form = self.app.get(reverse('admin:index')).form
        form['username'] = ADMIN_LOGIN
        form['password'] = ADMIN_PASS
        self.assertRedirects(form.submit(), reverse('admin:index'))
        self.app.get(reverse('admin:storage_project_changelist'))

    def _create_project(self, customer_id):
        url = reverse('admin:storage_project_add')
        form = self.app.get(url).forms['project_form']
        form['customer'] = customer_id
        form['short_name_ru'] = u'тест'
        form['short_name_en'] = u'test'
        self.assertRedirects(form.submit(), reverse('admin:storage_project_changelist'))

    def test_create(self):
        self._create_project(self.customer.pk)

    def test_existed_change_customer(self):
        self._create_project(self.customer.pk)
        url = reverse('admin:storage_project_change', args=(self.customer.pk,))
        form = self.app.get(url).forms['project_form']
        form['customer'] = self.customer2.pk
        form = form.submit(name='_continue', index=0).follow().forms['project_form']
        self.assertEqual(int(form['customer'].value), self.customer.pk)
