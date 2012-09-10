# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from django_webtest import WebTest

from .. models import Customer
from ... test_settings import *

__all__ = ('CustomerTest', )


class CustomerTest(WebTest):

    def setUp(self):
        self.admin = User.objects.create_superuser(Test.ADMIN_LOGIN, Test.ADMIN_EMAIL, Test.ADMIN_PASS)
        form = self.app.get(reverse('admin:index')).form
        form['username'] = Test.ADMIN_LOGIN
        form['password'] = Test.ADMIN_PASS
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
        # проверяем, что подставлен правильный заказчик
        form = self.app.get(url).click(linkid='related_project_add').forms['project_form']
        self.assertEqual(int(form['customer'].value), customer.pk)
        # проверяем, что подставлен правильный код
        code = '%sA01%s' % (customer.code, timezone.now().strftime('%y'))
        self.assertEqual(form['code'].value, code)

    def test_customer_types(self):
        PRIMARY = 1
        SECONDARY = 2
        self.customer = Customer.objects.create(
            customer_type=PRIMARY, partnership_type=1, code='0000', short_name='customer')
        self.customer2 = Customer.objects.create(
            customer_type=SECONDARY, partnership_type=2, code='0001', short_name='customer2')
        self.assertEqual({1: 1, 2: 1, 3: 0}, Customer.statistic.types())

    def test_customer_codes(self):
        PRIMARY = 1
        self.customer = Customer.objects.create(code='0000', customer_type=PRIMARY, partnership_type=1)

        response = self.app.get(reverse('get_customer_code'), params=dict(action='hc'))
        self.assertContains(response, '0001')
        response = self.app.get(reverse('get_customer_code'), params=dict(action='hm'))
        self.assertContains(response, '0001')

        self.customer = Customer.objects.create(code='0001', customer_type=PRIMARY, partnership_type=1)
        self.customer = Customer.objects.create(code='0003', customer_type=PRIMARY, partnership_type=1)
        self.customer = Customer.objects.create(code='0005', customer_type=PRIMARY, partnership_type=1)

        response = self.app.get(reverse('get_customer_code'), params=dict(action='hc'))
        self.assertContains(response, '0002')
        response = self.app.get(reverse('get_customer_code'), params=dict(action='hm'))
        self.assertContains(response, '0006')
