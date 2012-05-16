# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django_autoslug.fields import AutoSlugField

from src.users.models import CustomUser
from src.users.models import CustomGroup

from . managers import FinanceTransactionManager
from . managers import ProjectManager
from . managers import ProjectStatisticManager
from . managers import WalletStateManager


one_base = lambda values: list(enumerate(values, 1))

CUSTOMERS_CHOICES = one_base([_(u'primary'), _(u'secondary'), _(u'casual'), _(u'denied')])
PARTNERSHIP_CHOICES = one_base([_(u'internal'), _(u'master'), _(u'slave'), _(u'external')])
WALLET_CURRENCY_CHOICES = one_base([u'Рубли', u'Доллары'])
WALLET_TYPE = one_base([u'Безналичные рубли', u'Наличные рубли', u'Безналичные доллары', u'Наличные доллары'])
FINANCE_TRANSACTION_CHOICES = one_base([u'Приход', u'Расход'])
FINANCE_VAT_CHOICES = one_base([u'НДС включен', u'без НДС', u'НДС не взимается'])
PROJECT_TYPE_CHOICES = one_base([u'Офис', u'Квартира', u'Магазин', u'Фуд', u'Другое'])
PROJECT_STATUS_CHOICES = one_base([u'Потенциальный', u'Выигранный', u'Проигранный'])


class Workarea(models.Model):
    name = models.CharField(max_length=765)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = _(u'Work Area')
        verbose_name_plural = _(u'Work Areas')

    def __unicode__(self):
        return self.name


class Partner(models.Model):
    code = models.CharField(max_length=9)
    name = models.CharField(max_length=765)

    class Meta:
        verbose_name = _(u'Partner')
        verbose_name_plural = _(u'Partners')

    def __unicode__(self):
        return self.name


class Customer(models.Model):
    partner = models.ForeignKey(Partner, blank=True, null=True)
    workarea = models.ManyToManyField(Workarea, blank=True, null=True)
    customer_type = models.IntegerField(choices=CUSTOMERS_CHOICES)
    partnership_type = models.IntegerField(choices=PARTNERSHIP_CHOICES)
    code = models.CharField(max_length=5)
    short_name = models.CharField(max_length=255)
    long_name = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='customer/logo', max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = _(u'Customer')
        verbose_name_plural = _(u'Customers')

    def __unicode__(self):
        return self.short_name


class CompanyTeam(models.Model):
    u"""
    Модель компаний-исполнителей.
    """
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _(u'Staff: Company')
        verbose_name_plural = _(u'Staff: Companies')

    def __unicode__(self):
        return self.name


class JobType(models.Model):
    css = models.CharField(max_length=16)
    short_title = models.CharField(max_length=255)
    long_title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=32)

    class Meta:
        verbose_name = _(u'Job Type')
        verbose_name_plural = _(u'Job Types')

    def __unicode__(self):
        return self.short_title


class Project(models.Model):
    customer = models.ForeignKey(Customer)
    address = models.CharField(max_length=255, blank=True, null=True)
    staff = models.ManyToManyField(CustomUser, through='Membership')
    job_type = models.ManyToManyField(JobType)
    short_name = models.CharField(max_length=128)
    long_name = models.TextField(blank=True, null=True)
    ptype = models.IntegerField(choices=PROJECT_TYPE_CHOICES)
    status = models.IntegerField(choices=PROJECT_STATUS_CHOICES)
    desc_short = models.TextField(blank=True, null=True)
    desc_long = models.TextField(blank=True, null=True)
    tasks = models.TextField(blank=True, null=True)
    problems = models.TextField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    made_for = models.CharField(max_length=255, blank=True, null=True)
    object_square = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)
    duration_production = models.IntegerField(default=0)
    duration_changes = models.IntegerField(default=0)
    duration_discussion = models.IntegerField(default=0)
    duration_other = models.IntegerField(default=0)
    productivity = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)
    begin = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    price_average = models.DecimalField(max_digits=19, decimal_places=4, default=0.0, help_text=u'Цена за квадратный метр')
    price_full = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)
    currency = models.IntegerField(choices=WALLET_CURRENCY_CHOICES)
    exchange_rate = models.DecimalField(max_digits=19, decimal_places=4, default=1.0)
    is_public = models.BooleanField(default=False, help_text=u'Публичный проект')
    is_archived = models.BooleanField(default=False, help_text=u'Архивный')
    is_finished = models.BooleanField(default=False, help_text=u'Завершённый')
    in_stats = models.BooleanField(default=True, help_text=u'Учитывается в статистике')
    registered = models.DateTimeField(auto_now_add=True)

    slug = AutoSlugField(populate_from=('short_name',), unique=True, max_length=255, overwrite=True)

    objects = ProjectManager()
    statistic = ProjectStatisticManager()

    class Meta:
        verbose_name = u'Project'
        verbose_name_plural = u'Projects'

    def __unicode__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse('frontend:project', kwargs=dict(slug=self.slug))

    def save(self, *args, **kwargs):
        try:
            self.productivity = self.object_square / self.duration_production
        except ZeroDivisionError:
            self.productivity = 0.0

        try:
            self.price_average = self.price_full / self.object_square
        except ZeroDivisionError:
            self.price_average = 0.0

        return super(Project, self).save(*args, **kwargs)

    @property
    def teaser(self):
        u"""Возвращает главное изображение проекта."""
        try:
            return self.projectimage_set.get(is_teaser=True)
        except self.DoesNotExist:
            return None

    @property
    def price_meter(self):
        u"""Цена за квадратный метр."""
        return self.price_full / self.object_square

    @property
    def duration_full(self):
        u"""Полные трудозатраты, в часах."""
        return self.duration_production + self.duration_changes + self.duration_discussion + self.duration_other

    @property
    def production_percent(self):
        u"""Процент производственного времени."""
        return self.duration_production * 100 / self.duration_full

    @property
    def meters_per_hour(self):
        u"""Скорость проектирования, метров в час."""
        return self.object_square / self.duration_production

    @property
    def speed(self):
        u"""Скорость проекта, метров в день."""
        return self.object_square / self.duration_full


class Membership(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(CustomUser, blank=True, null=True)
    company = models.ForeignKey(CompanyTeam, blank=True, null=True)
    role = models.ManyToManyField(CustomGroup, verbose_name=_(u'Role'))
    url = models.URLField(blank=True, null=True)
    joined_at = models.DateTimeField(verbose_name=_(u'Joined'), auto_now_add=True)
    leaved_at = models.DateTimeField(verbose_name=_(u'Leaved'), blank=True, null=True)


def upload_with_name(instance, filename):
    return u'project/image/%s/%s' % (instance.project.slug, filename)


class ProjectImage(models.Model):
    project = models.ForeignKey(Project)
    position = models.IntegerField()
    image = models.ImageField(upload_to=upload_with_name, max_length=255)
    comment = models.CharField(max_length=255, blank=True, null=True)
    is_teaser = models.BooleanField()
    is_pro6 = models.BooleanField()
    is_publish = models.BooleanField()


class FinanceTransaction(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    wallet = models.IntegerField(choices=WALLET_TYPE)
    contract = models.CharField(max_length=255)
    contractor = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    description = models.CharField(max_length=255)
    transaction_type = models.IntegerField(choices=FINANCE_TRANSACTION_CHOICES)
    transaction_vat = models.IntegerField(choices=FINANCE_VAT_CHOICES)
    exchange_rate = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    done_at = models.DateTimeField()
    registered = models.DateTimeField(auto_now_add=True)

    objects = FinanceTransactionManager()

    class Meta:
        verbose_name = u'Finance Transaction'
        verbose_name_plural = u'Finance Transactions'

    def __unicode__(self):
        return u'%s, %s, %0.2f' % (self.get_wallet_display(), self.get_transaction_type_display(), self.amount)


class WalletState(models.Model):
    wallet = models.IntegerField(choices=WALLET_TYPE)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    registered = models.DateTimeField(auto_now_add=True)

    objects = WalletStateManager()

    class Meta:
        verbose_name = u'Wallet State'
        verbose_name_plural = u'Wallet States'

    def __unicode__(self):
        return u'%s (%f)' % (self.get_wallet_display(), self.amount)


class Recommendation(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=32)
    email = models.CharField(max_length=128)

    class Meta:
        verbose_name = u'Recommendation'
        verbose_name_plural = u'Recommendations'

    def __unicode__(self):
        return self.name
