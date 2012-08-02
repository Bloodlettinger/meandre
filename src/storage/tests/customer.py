# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_webtest import WebTest

from .. models import Customer
from . settings import *

__all__ = ('CustomerTest', )


class CustomerTest(WebTest):

    def setUp(self):
        self.admin = User.objects.create_superuser(ADMIN_LOGIN, ADMIN_EMAIL, ADMIN_PASS)
        form = self.app.get(reverse('admin:index')).form
        form['username'] = ADMIN_LOGIN
        form['password'] = ADMIN_PASS
        self.assertRedirects(form.submit(), reverse('admin:index'))
        self.app.get(reverse('admin:storage_customer_changelist'))

    def test_create(self):
        url = reverse('admin:storage_customer_add')
        form = self.app.get(url).forms['customer_form']
        form['customer_type'] = 1
        form['partnership_type'] = 1
        form['code'] = '0000'
        form['short_name_ru'] = u'заказчик'
        form['short_name_en'] = u'customer'
        self.assertRedirects(form.submit(), reverse('admin:storage_customer_changelist'))

    def test_create_related_project(self):
        customer = Customer.objects.create(
            customer_type=1,
            partnership_type=1,
            code='0000',
            short_name='customer'
            )
        url = reverse('admin:storage_customer_change', args=(customer.pk, ))
        form = self.app.get(url).click(linkid='related_project_add').forms['project_form']
        self.assertEqual(int(form['customer'].value), customer.pk)
