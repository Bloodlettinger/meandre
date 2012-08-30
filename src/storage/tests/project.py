# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone

import factory
from django_webtest import WebTest

from .. models import Customer, Project
from ... test_settings import *

__all__ = ('ProjectTest', )


CREATED, BEGIN, END, FINISHED = map(
    lambda x: timezone.datetime(*x).date(),
    ((2012, 1, 1), (2012, 1, 2), (2012, 1, 3), (2012, 1, 4)))


class CustomerFactory(factory.Factory):
    FACTORY_FOR = Customer

    customer_type = 1  # primary
    partnership_type = 1  # internal


class ProjectFactory(factory.Factory):
    FACTORY_FOR = Project

    customer = factory.LazyAttribute(lambda x: CustomerFactory())
    is_public = True
    price_full = 0
    exchange_rate = 0
    productivity = 0
    price_average = 0


class ProjectTest(WebTest):

    def setUp(self):
        self.admin = User.objects.create_superuser(Test.ADMIN_LOGIN, Test.ADMIN_EMAIL, Test.ADMIN_PASS)
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
        form['username'] = Test.ADMIN_LOGIN
        form['password'] = Test.ADMIN_PASS
        self.assertRedirects(form.submit(), reverse('admin:index'))
        self.app.get(reverse('admin:storage_project_changelist'))

    def _create_project(self, customer_id):
        url = reverse('admin:storage_project_add')
        form = self.app.get(url).forms['project_form']
        form['customer'] = customer_id
        form['short_name_ru'] = u'тест'
        form['short_name_en'] = u'test'
        form['reg_date'] = CREATED
        form['begin'] = BEGIN
        form['end'] = END
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

    def test_finished_at(self):
        project = ProjectFactory(short_name='test')
        assert project.finished_at is None
        project.is_finished = True
        project.save()
        assert project.finished_at is not None

    def test_dates(self):
        project = ProjectFactory(
            short_name_en='test', short_name_ru='test',
            reg_date=CREATED, begin=BEGIN, end=END, finished_at=FINISHED
        )

        url = reverse('admin:storage_project_change', args=(project.pk, ))
        form = self.app.get(url).forms['project_form']

        form['reg_date'] = BEGIN
        form['begin'] = CREATED
        response = form.submit(name='_continue', index=0)
        el = response.lxml.xpath('//ul[@class="errorlist"]')
        self.assertEqual(1, len(el))

        form['begin'] = END
        form['end'] = BEGIN
        response = form.submit(name='_continue', index=0)
        el = response.lxml.xpath('//ul[@class="errorlist"]')
        self.assertEqual(1, len(el))

        form['reg_date'] = CREATED
        form['begin'] = BEGIN
        form['end'] = END
        response = form.submit(name='_save', index=0)
        self.assertRedirects(response, reverse('admin:storage_project_changelist'))
