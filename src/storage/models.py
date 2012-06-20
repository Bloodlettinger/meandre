# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import User

from django_autoslug.fields import AutoSlugField

from .. users.models import CustomUser

from . managers import FinanceTransactionManager
from . managers import ProjectManager
from . managers import ProjectStatisticManager
from . managers import WalletStateManager


one_base = lambda values: list(enumerate(values, 1))

CUSTOMERS_CHOICES = one_base([_(u'primary'), _(u'secondary'), _(u'casual'), _(u'denied')])
PARTNERSHIP_CHOICES = one_base([_(u'internal'), _(u'master'), _(u'slave'), _(u'external')])
WALLET_CURRENCY_CHOICES = one_base([_(u'Roubles'), _(u'Dollars')])
WALLET_TYPE = one_base([_(u'Roubles Bank Account'), _(u'Roubles Cash Account'), _(u'Dollars Bank Account'), _(u'Dollars Cash Account')])
FINANCE_TRANSACTION_CHOICES = one_base([_(u'Income'), _(u'Expense')])
FINANCE_VAT_CHOICES = one_base([_(u'with VAT'), _(u'without VAT'), _(u'VAT not chargable')])
PROJECT_TYPE_CHOICES = one_base([_(u'Office'), _(u'Flat'), _(u'Shop'), _(u'Food'), _(u'Other')])
PROJECT_STATUS_CHOICES = one_base([_(u'Potential'), _(u'Winned'), _(u'Loosed')])


class Workarea(models.Model):
    name = models.CharField(max_length=765, verbose_name=pgettext_lazy('item', u'Name'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'Enabled'))

    class Meta:
        verbose_name = _(u'Work Area')
        verbose_name_plural = _(u'Work Areas')

    def __unicode__(self):
        return self.name


class Partner(models.Model):
    code = models.CharField(max_length=9, verbose_name=_(u'Code'))
    name = models.CharField(max_length=765, verbose_name=pgettext_lazy('human', u'Name'))

    class Meta:
        verbose_name = _(u'Partner')
        verbose_name_plural = _(u'Partners')

    def __unicode__(self):
        return self.name


class Customer(models.Model):
    partner = models.ForeignKey(Partner, blank=True, null=True, verbose_name=_(u'Partner'))
    workarea = models.ManyToManyField(Workarea, blank=True, null=True, verbose_name=_(u'Work Area'))
    customer_type = models.IntegerField(choices=CUSTOMERS_CHOICES, verbose_name=_(u'Type'))
    partnership_type = models.IntegerField(choices=PARTNERSHIP_CHOICES, verbose_name=_(u'Partnership'))
    code = models.CharField(max_length=5, verbose_name=_(u'Code'))
    short_name = models.CharField(max_length=255, verbose_name=pgettext_lazy('item', u'Name (short)'))
    long_name = models.TextField(blank=True, null=True, verbose_name=pgettext_lazy('item', u'Name (long)'))
    logo = models.ImageField(upload_to='customer/logo', max_length=255, blank=True, null=True, verbose_name=_(u'Logo'))
    url = models.URLField(blank=True, null=True)
    registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _(u'Customer')
        verbose_name_plural = _(u'Customers')

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.short_name)


class CompanyTeam(models.Model):
    u"""
    Модель компаний-исполнителей.
    """
    name = models.CharField(max_length=255, verbose_name=pgettext_lazy('item', u'Name'))

    class Meta:
        verbose_name = _(u'Staff: Company')
        verbose_name_plural = _(u'Staff: Companies')

    def __unicode__(self):
        return self.name


class JobType(models.Model):
    css = models.CharField(max_length=16, verbose_name=_(u'CSS class'))
    short_title = models.CharField(max_length=255, verbose_name=pgettext_lazy('item', u'Name (short)'))
    long_title = models.CharField(max_length=255, verbose_name=pgettext_lazy('item', u'Name (long)'))
    description = models.TextField(verbose_name=_(u'Description'))
    duration = models.CharField(max_length=32, verbose_name=_(u'Duration'))

    class Meta:
        verbose_name = _(u'Job Type')
        verbose_name_plural = _(u'Job Types')

    def __unicode__(self):
        return self.short_title


class Project(models.Model):
    customer = models.ForeignKey(Customer, verbose_name=_(u'Customer'))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_(u'Address'))
    staff = models.ManyToManyField(CustomUser, through='Membership', verbose_name=_(u'Staff'))
    job_type = models.ManyToManyField(JobType, verbose_name=_(u'Job Type'))
    short_name = models.CharField(max_length=128, verbose_name=pgettext_lazy('item', u'Name (short)'))
    long_name = models.CharField(max_length=512, blank=True, null=True, verbose_name=pgettext_lazy('item', u'Name (long)'))
    ptype = models.IntegerField(choices=PROJECT_TYPE_CHOICES, default=1, verbose_name=_(u'Type'))
    status = models.IntegerField(choices=PROJECT_STATUS_CHOICES, default=1, verbose_name=_(u'Status'))
    desc_short = models.TextField(blank=True, null=True, verbose_name=_(u'Description (short)'))
    desc_long = models.TextField(blank=True, null=True, verbose_name=_(u'Description (long)'))
    tasks = models.TextField(blank=True, null=True, verbose_name=_(u'Tasks'))
    problems = models.TextField(blank=True, null=True, verbose_name=_(u'Problems'))
    results = models.TextField(blank=True, null=True, verbose_name=_(u'Results'))
    made_for = models.CharField(max_length=255, blank=True, null=True, verbose_name=_(u'Made for'))
    object_square = models.IntegerField(default=0, verbose_name=pgettext_lazy('object', u'Square'), help_text=_(u'Square meters'))
    duration_production = models.IntegerField(default=0, verbose_name=pgettext_lazy('duration', u'Production'), help_text=_(u'In hours'))
    duration_changes = models.IntegerField(default=0, verbose_name=pgettext_lazy('duration', u'Changes'), help_text=_(u'In hours'))
    duration_discussion = models.IntegerField(default=0, verbose_name=pgettext_lazy('duration', u'Discussion'), help_text=_(u'In hours'))
    duration_other = models.IntegerField(default=0, verbose_name=pgettext_lazy('duration', u'Other'), help_text=_(u'In hours'))
    begin = models.DateField(blank=True, null=True, verbose_name=_(u'Begin'))
    end = models.DateField(blank=True, null=True, verbose_name=_(u'End'))
    price_full = models.DecimalField(max_digits=19, decimal_places=2, default=0, verbose_name=_(u'Price'))
    currency = models.IntegerField(choices=WALLET_CURRENCY_CHOICES, verbose_name=_(u'Currency'))
    exchange_rate = models.DecimalField(max_digits=19, decimal_places=2, default=1, verbose_name=_(u'Exchange Rate'))
    is_public = models.BooleanField(default=False, verbose_name=_(u'Public'), help_text=_(u'Check if this project is public'))
    is_archived = models.BooleanField(default=False, verbose_name=_(u'Archived'), help_text=_(u'Check if this project is archived'))
    is_finished = models.BooleanField(default=False, verbose_name=_(u'Finished'), help_text=_(u'Check if this prohect is finished'))
    in_stats = models.BooleanField(default=True, verbose_name=_(u'Statistic'), help_text=_(u'Check if this project is shown in statistics'))
    registered = models.DateTimeField(auto_now_add=True)

    # вычисляемые поля, см. метод save()
    productivity = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    price_average = models.DecimalField(max_digits=19, decimal_places=2, default=0, help_text=_(u'Price for square meter'))

    slug = AutoSlugField(populate_from=('short_name',), unique=True, max_length=255, overwrite=True)

    objects = ProjectManager()
    statistic = ProjectStatisticManager()

    class Meta:
        verbose_name = _(u'Project')
        verbose_name_plural = _(u'Projects')

    def __unicode__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse('frontend:project', kwargs=dict(slug=self.slug))

    def save(self, *args, **kwargs):
        try:
            self.productivity = self.object_square / self.duration_production
        except:
            self.productivity = 0

        try:
            self.price_average = self.price_full / self.object_square
        except:
            self.price_average = 0

        return super(Project, self).save(*args, **kwargs)

    @property
    def teaser(self):
        u"""Возвращает главное изображение проекта."""
        try:
            return self.projectimage_set.get(is_teaser=True)
        except self.DoesNotExist:
            return None

    @property
    def pro6(self):
        u"""Возвращает изображение проекта для витрины."""
        try:
            return self.projectimage_set.get(is_pro6=True)
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

    @property
    def created(self):
        u"""Дата создания проекта."""
        return self.registered.date


class MembershipRole(models.Model):
    title = models.CharField(max_length=64, verbose_name=_(u'Title'))

    class Meta:
        verbose_name = _(u'Membership Role')
        verbose_name_plural = _(u'Membership Roles')

    def __unicode__(self):
        return self.title


class Membership(models.Model):
    project = models.ForeignKey(Project, verbose_name=_(u'Project'))
    user = models.ForeignKey(CustomUser, blank=True, null=True, verbose_name=_(u'User'))
    company = models.ForeignKey(CompanyTeam, blank=True, null=True, verbose_name=_(u'Company'))
    role = models.ManyToManyField(MembershipRole, verbose_name=_(u'Role'))
    url = models.URLField(blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Joined'))
    leaved_at = models.DateTimeField(blank=True, null=True, verbose_name=_(u'Leaved'))


def upload_with_name(instance, filename):
    u"""Возвращает путь для загружаемого изображения, учитывая название проекта."""
    return u'project/image/%s/%s' % (instance.project.slug, filename)


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, verbose_name=_(u'Project'))
    position = models.IntegerField(verbose_name=_(u'Position'))
    image = models.ImageField(upload_to=upload_with_name, max_length=255, verbose_name=_(u'Image Path'))
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name=_(u'Comment'))
    is_teaser = models.BooleanField(verbose_name=_(u'Teaser'))
    is_pro6 = models.BooleanField(verbose_name=_(u'Pro6 Block'))
    is_publish = models.BooleanField(verbose_name=_(u'Public'))


class FinanceTransaction(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'Registrator'))
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name=_(u'Parent'))
    wallet = models.IntegerField(choices=WALLET_TYPE, verbose_name=_(u'Wallet'))
    amount = models.DecimalField(max_digits=19, decimal_places=2, verbose_name=_(u'Amount'))
    description = models.CharField(max_length=255, verbose_name=_(u'Description'))
    transaction_type = models.IntegerField(choices=FINANCE_TRANSACTION_CHOICES, verbose_name=_(u'Type'))
    transaction_vat = models.IntegerField(choices=FINANCE_VAT_CHOICES, verbose_name=_(u'VAT'))
    exchange_rate = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, verbose_name=_(u'Exchange Rate'))
    contract = models.CharField(max_length=255, blank=True, null=True, verbose_name=_(u'Contract'))
    contractor = models.CharField(max_length=255, blank=True, null=True, verbose_name=_(u'Contractor'))
    done_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Done'))
    registered = models.DateTimeField(auto_now_add=True)

    objects = FinanceTransactionManager()

    class Meta:
        verbose_name = _(u'Finance Transaction')
        verbose_name_plural = _(u'Finance Transactions')

    def __unicode__(self):
        return u'%s, %s, %0.2f' % (self.get_wallet_display(), self.get_transaction_type_display(), self.amount)


class WalletState(models.Model):
    wallet = models.IntegerField(choices=WALLET_TYPE, verbose_name=_(u'Wallet'))
    amount = models.DecimalField(max_digits=19, decimal_places=2, verbose_name=_(u'Amount'))
    moment = models.DateField(verbose_name=_(u'Moment'))
    registered = models.DateTimeField(auto_now_add=True)

    objects = WalletStateManager()

    class Meta:
        verbose_name = _(u'Wallet State')
        verbose_name_plural = _(u'Wallet States')

    def __unicode__(self):
        return u'%s (%f)' % (self.get_wallet_display(), self.amount)


class WalletStateReport(models.Model):
    u"""
    Фейковая модель для вывода текущего состояния счетов.
    """
    class Meta:
        verbose_name = _(u'Report: Wallet State')
        verbose_name_plural = _(u'Report: Wallet States')
        managed = False


class Recommendation(models.Model):
    name = models.CharField(verbose_name=pgettext_lazy('human', u'Name'),  max_length=128)
    phone = models.CharField(verbose_name=_(u'Phone'), max_length=32)
    email = models.CharField(verbose_name=_(u'E-mail'), max_length=128)

    class Meta:
        verbose_name = _(u'Recommendation')
        verbose_name_plural = _(u'Recommendations')

    def __unicode__(self):
        return self.name
