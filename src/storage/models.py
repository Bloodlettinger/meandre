# -*- coding: utf-8 -*-

from datetime import date

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils import timezone

from django_autoslug.fields import AutoSlugField

from .. users.models import CustomUser
from .. uploader.models import Queue as ImageQueue

from . managers import FinanceTransactionManager
from . managers import ProjectManager
from . managers import ProjectStatisticManager
from . managers import CustomerStatisticManager
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

ICON_TPL = u'<img src="%(static)simg/site/%(value)s-emboss-32.png" title="%(title)s"/>'
default = dict(static=settings.STATIC_URL)
PROJECT_TYPE_ICONS = one_base([
    mark_safe(ICON_TPL % dict(default, value='work', title=_(u'Office'))),
    mark_safe(ICON_TPL % dict(default, value='home', title=_(u'Flat'))),
    mark_safe(ICON_TPL % dict(default, value='shop', title=_(u'Shop'))),
    mark_safe(ICON_TPL % dict(default, value='entertainment', title=_(u'Food'))),
    mark_safe(ICON_TPL % dict(default, value='other', title=_(u'Other'))),
    ])


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

    objects = models.Manager()
    statistic = CustomerStatisticManager()

    class Meta:
        verbose_name = _(u'Customer')
        verbose_name_plural = _(u'Customers')

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.short_name)

    def last_public_project(self):
        u"""
        Метод для выдачи последнего публичного проекта.
        """
        try:
            project = self.project_set.public().order_by('-reg_date')[0]
        except IndexError:
            return None
        else:
            return project.get_absolute_url()


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
    code = models.CharField(max_length=9, unique=True, verbose_name=_(u'Code'))
    customer = models.ForeignKey(Customer, verbose_name=_(u'Customer'))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_(u'Address'))
    staff_roles = models.ManyToManyField('MembershipRole', through='Membership', verbose_name=_(u'Staff'))
    job_type = models.ManyToManyField(JobType, blank=True, null=True, verbose_name=_(u'Job Type'))
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
    price_full = models.DecimalField(max_digits=19, decimal_places=2, default=0, verbose_name=_(u'Price'), help_text=_(u'Fractional part is not required'))
    currency = models.IntegerField(choices=WALLET_CURRENCY_CHOICES, default=1, verbose_name=_(u'Currency'))
    exchange_rate = models.DecimalField(max_digits=19, decimal_places=2, default=1.0, verbose_name=_(u'Exchange Rate'))
    is_public = models.BooleanField(default=False, verbose_name=_(u'Public'), help_text=_(u'Check if this project is public'))
    is_archived = models.BooleanField(default=False, verbose_name=_(u'Archived'), help_text=_(u'Check if this project is archived'))
    is_finished = models.BooleanField(default=False, verbose_name=_(u'Finished'), help_text=_(u'Check if this prohect is finished'))
    in_stats = models.BooleanField(default=True, verbose_name=_(u'Statistic'), help_text=_(u'Check if this project is shown in statistics'))
    registered = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Registered'))
    reg_date = models.DateField(default=timezone.now, verbose_name=_(u'Registered'),
        help_text=_(u'Keep it empty to fill automaticly.'))

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

        # при создании модели необходимо сгенерировать код проекта,
        # если он не был явно указан
        if not self.pk and 0 == len(self.code):
            cust_id = self.customer.code
            count = Project.objects.filter(customer__code=cust_id,
                code__iregex=r'^[0-9]{4}A[0-9]{4}').count()
            tpl = '{customer_code:0>4}A{project_number:0>2}{year:0>2}'
            context = dict(
                customer_code=cust_id,
                project_number=count + 1,
                year=date.today().strftime('%y'))
            self.code = tpl.format(**context)

        return super(Project, self).save(*args, **kwargs)

    @property
    def teaser(self):
        u"""Возвращает главное изображение проекта."""
        try:
            return ImageQueue.objects.get(teaser=True, tags=self.code)
        except self.DoesNotExist:
            return None

    @property
    def pro6(self):
        u"""Возвращает изображение проекта для витрины."""
        return self.teaser

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


STAFF_TYPE_PERSON = 1
STAFF_TYPE_COMPANY = 2
STAFF_TYPE_CHOICES = (
    (STAFF_TYPE_PERSON, 'person'),
    (STAFF_TYPE_COMPANY, 'company'))


class Staff(models.Model):
    u"""
    Базовая модель члена команды: Человек или компания.

    Поле which используется для быстрого определения типа объекта.
    """
    which = models.IntegerField(choices=STAFF_TYPE_CHOICES)
    phone = models.CharField(max_length=32, blank=True, null=True, verbose_name=_(u'Phone'))
    email = models.CharField(max_length=128, blank=True, null=True, verbose_name=_(u'E-mail'))
    address = models.CharField(max_length=256, blank=True, null=True, verbose_name=_(u'Address'))

    slave_models = ('staffperson', 'staffcompany')

    class Meta:
        verbose_name = u'%s: %s' % (_(u'Staff'), _(u'Abstract'))
        verbose_name_plural = u'%s: %s' % (_(u'Staff'), _(u'Abstract'))

    def __slaves__(self):
        for slave in self.slave_models:
            try:
                # подгружаем дочернюю модель
                return (slave, getattr(self, slave))
            except models.ObjectDoesNotExist:
                pass  # проверяем следующую
        # не нашли
        raise models.ObjectDoesNotExist(_(u'It seems this method is called on base model '
            'instance or some previous action broke database consistent.'))

    def __unicode__(self):
        name, obj = self.__slaves__()
        return obj.__unicode__()

    @property
    def url(self):
        name, obj = self.__slaves__()
        return getattr(obj, 'site', None)


class StaffPerson(Staff):
    u"""
    Модель члена команды: Человек.
    """
    first_name = models.CharField(max_length=64, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=64, verbose_name=_('Last Name'))
    company = models.CharField(max_length=256, blank=True, null=True, verbose_name=_(u'Company'))

    class Meta:
        verbose_name = u'%s: %s' % (_(u'Staff'), _(u'Person'))
        verbose_name_plural = u'%s: %s' % (_(u'Staff'), _(u'Persons'))

    def __unicode__(self):
        value = u'%s %s' % (self.first_name, self.last_name)
        if self.company and self.company != '':
            value = u'%s (%s)' % (value, self.company)
        return value

    def save(self, *args, **kwargs):
        self.which = STAFF_TYPE_PERSON
        super(StaffPerson, self).save(*args, **kwargs)


class StaffCompany(Staff):
    u"""
    Модель члена команды: Компания.
    """
    title = models.CharField(max_length=64, verbose_name=_('Title'))
    site = models.URLField(verbose_name=u'Site URL')

    class Meta:
        verbose_name = u'%s: %s' % (_(u'Staff'), _(u'Company'))
        verbose_name_plural = u'%s: %s' % (_(u'Staff'), _(u'Companies'))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.which = STAFF_TYPE_COMPANY
        super(StaffCompany, self).save(*args, **kwargs)


class MembershipRole(models.Model):
    title = models.CharField(max_length=64, verbose_name=_(u'Title'))

    class Meta:
        verbose_name = _(u'Membership Role')
        verbose_name_plural = _(u'Membership Roles')

    def __unicode__(self):
        return self.title


class Membership(models.Model):
    project = models.ForeignKey(Project, verbose_name=_(u'Project'))
    role = models.ForeignKey(MembershipRole, verbose_name=_(u'Role'))
    staff = models.ManyToManyField(Staff, verbose_name=_(u'User'))
    position = models.IntegerField(verbose_name=_(u'Position'))
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Joined'))
    leaved_at = models.DateTimeField(blank=True, null=True, verbose_name=_(u'Leaved'))

    class Meta:
        verbose_name = _(u'Membership')
        verbose_name_plural = _(u'Membership')
        ordering = ('position', )


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
    done_at = models.DateTimeField(verbose_name=_(u'Done'))
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
