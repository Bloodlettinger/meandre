# -*- coding: utf-8 -*-

import re
import decimal
from datetime import date

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.contrib import messages

from django_autoslug.fields import AutoSlugField

from .. uploader.models import Queue as ImageQueue

from . managers import FinanceTransactionManager
from . managers import ProjectManager
from . managers import ProjectStatisticManager
from . managers import CustomerStatisticManager
from . managers import WalletStateManager


PROJECT_CODE_RE = re.compile(r'^\d{4}A(?P<ordering>\d{2})\d{2}$')

one_base = lambda values: list(enumerate(values, 1))

CUSTOMERS_CHOICES = one_base([_(u'primary'), _(u'secondary'), _(u'casual'), _(u'denied')])

PARTNERSHIP_INTERNAL = 1
PARTNERSHIP_MASTER = 2
PARTNERSHIP_SLAVE = 3
PARTNERSHIP_EXTERNAL = 4
PARTNERSHIP_CHOICES = (
    (PARTNERSHIP_INTERNAL, _(u'internal')),
    (PARTNERSHIP_MASTER, _(u'master')),
    (PARTNERSHIP_SLAVE, _(u'slave')),
    (PARTNERSHIP_EXTERNAL, _(u'external'))
)
PARTNERSHIP_SIGNS = {
    PARTNERSHIP_INTERNAL: '&nbsp;',
    PARTNERSHIP_MASTER: '&larr;',
    PARTNERSHIP_SLAVE: '&rarr;',
    PARTNERSHIP_EXTERNAL: '&times;',
}

WALLET_CURRENCY_ROUBLES = 1
WALLET_CURRENCY_DOLLARS = 2
WALLET_CURRENCY_CHOICES = (
    (WALLET_CURRENCY_ROUBLES, _(u'Roubles')),
    (WALLET_CURRENCY_DOLLARS, _(u'Dollars'))
)

WALLET_TYPE = one_base([_(u'Roubles Bank Account'), _(u'Roubles Cash Account'), _(u'Dollars Bank Account'), _(u'Dollars Cash Account')])
FINANCE_TRANSACTION_CHOICES = one_base([_(u'Income'), _(u'Expense')])
FINANCE_VAT_CHOICES = one_base([_(u'with VAT'), _(u'without VAT'), _(u'VAT not chargable')])
PROJECT_TYPE_CHOICES = one_base([_(u'Office'), _(u'Flat'), _(u'Shop'), _(u'Food'), _(u'Other')])

PROJECT_STATUS_POTENTIAL = 1
PROJECT_STATUS_WON = 2
PROJECT_STATUS_LOST = 3
PROJECT_STATUS_CHOICES = (
    (PROJECT_STATUS_POTENTIAL, _(u'Potential')),
    (PROJECT_STATUS_WON, _(u'Won')),
    (PROJECT_STATUS_LOST, _(u'Lost'))
)

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
    logo = models.ImageField(upload_to='customer/logo', max_length=255, blank=True, null=True, verbose_name=_(u'Logo'),
        help_text=_(u'Resize it to 135х93 and set background to transparent or white.'))
    url = models.URLField(blank=True, null=True)
    registered = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    statistic = CustomerStatisticManager()

    class Meta:
        verbose_name = _(u'Customer')
        verbose_name_plural = _(u'Customers')

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.short_name)

    def is_translated(self, lang):
        from .. translation import CustomerOpts as opts
        for field in opts.fields:
            field_name = u'%s_%s' % (field, lang)
            value = getattr(self, field_name)
            if value is None or 0 == len(value.strip()):
                return False
        return True

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

    @staticmethod
    def generate_code(lowest=True):
        seq = map(
            lambda x: int(x[0]),
            Customer.objects.values_list('code'))
        if 0 == len(seq):
            seq = (0, )
        # если затребован минимальный номер, то ищем "дырку" в последовательности
        if 1 < len(seq) and lowest:
            i = iter(seq)
            f = next(i)
            while True:
                try:
                    n = next(i)
                    if 1 == n - f:
                        f = n
                        continue
                    return f + 1
                    break
                except StopIteration:
                    pass
        # если "дырку" найти не получилось, то берём следующий по списку номер
        return max(seq) + 1


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

    def is_translated(self, lang):
        from .. translation import JobTypeOpts as opts
        for field in opts.fields:
            field_name = u'%s_%s' % (field, lang)
            value = getattr(self, field_name)
            if value is None or 0 == len(value.strip()):
                return False
        return True


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
    object_square = models.IntegerField(default=0, verbose_name=pgettext_lazy('object', u'Area'), help_text=_(u'Square meters'))
    duration_production = models.IntegerField(default=0, verbose_name=pgettext_lazy('duration', u'Production'), help_text=_(u'In hours'))
    duration_changes = models.IntegerField(default=0, verbose_name=pgettext_lazy('duration', u'Changes'), help_text=_(u'In hours'))
    duration_discussion = models.IntegerField(default=0, verbose_name=pgettext_lazy('duration', u'Discussion'), help_text=_(u'In hours'))
    duration_other = models.IntegerField(default=0, verbose_name=pgettext_lazy('duration', u'Other'), help_text=_(u'In hours'))
    begin = models.DateField(blank=True, null=True, verbose_name=_(u'Begin'))
    end = models.DateField(blank=True, null=True, verbose_name=_(u'End'))
    price_full = models.DecimalField(max_digits=19, decimal_places=2, default=0, verbose_name=_(u'Price'), help_text=_(u'Fractional part is not required'))
    currency = models.IntegerField(choices=WALLET_CURRENCY_CHOICES, default=1, verbose_name=_(u'Currency'))
    exchange_rate = models.DecimalField(max_digits=19, decimal_places=2, default=1.0, verbose_name=_(u'Exchange Rate'))
    is_public_ru = models.BooleanField(default=False, verbose_name=_(u'Public for RU area'), help_text=_(u'Check if this project is public for russian auditory'))
    is_public_en = models.BooleanField(default=False, verbose_name=_(u'Public for EN area'), help_text=_(u'Check if this project is public for english auditory'))
    is_archived = models.BooleanField(default=False, verbose_name=_(u'Archived'), help_text=_(u'Check if this project is archived'))
    is_finished = models.BooleanField(default=False, verbose_name=_(u'Finished'), help_text=_(u'Check if this prohect is finished'))
    in_stats = models.BooleanField(default=True, verbose_name=_(u'Statistic'), help_text=_(u'Check if this project is shown in statistics'))
    registered = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Registered'))
    reg_date = models.DateField(default=timezone.now, verbose_name=_(u'Registered'),
        help_text=_(u'Keep it empty to fill automaticly.'))
    finished_at = models.DateField(blank=True, null=True, verbose_name=_(u'Finished'))

    # вычисляемые поля, см. метод save()
    productivity = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    price_average = models.DecimalField(max_digits=19, decimal_places=2, default=0, help_text=_(u'Price for square meter'))

    slug = AutoSlugField(populate_from=('short_name',), unique=True, max_length=255, overwrite=True)

    # поле для работы сортировки проектов на странице заказчика
    ordering = models.IntegerField(default=0)

    objects = ProjectManager()
    statistic = ProjectStatisticManager()

    class Meta:
        verbose_name = _(u'Project')
        verbose_name_plural = _(u'Projects')
        ordering = ('-reg_date', )

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
            self.code = Project.code_factory(code=self.customer.code)

        # фиксируем дату закрытия проекта
        if self.is_finished and not self.end:
            self.end = timezone.now()
        elif self.end and not self.is_finished:
            self.is_finished = True

        if self.is_finished and not self.finished_at:
            self.finished_at = timezone.now()

        # сохраняем информацию о сортировке
        re_obj = PROJECT_CODE_RE.search(self.code)
        if re_obj:
            self.ordering = int(re_obj.group('ordering'))

        # проверка настроек публичности и их коррекция по необходимости
        try:
            request = kwargs.pop('request')
        except KeyError:
            request = None

        if self.teaser is None:
            for lang, name in settings.LANGUAGES:
                field_name = u'is_public_%s' % lang
                setattr(self, field_name, False)
            if request:
                messages.warning(request,
                    _(u'The project "%(name)s" is hidden for auditory.') % {'name': self.short_name})
        else:
            fields = ['address', 'short_name']
            for lang, name in settings.LANGUAGES:
                field_name = u'is_public_%s' % lang
                value_old = getattr(self, field_name, False)
                value_new = self.is_ready_to_public(lang, fields)
                if value_old != value_new:
                    setattr(self, field_name, value_new)
                    if request:
                        params = dict(
                            name=self.short_name,
                            state=_(u'visible') if value_new else _(u'hidden'),
                            lang=lang.upper()
                        )
                        messages.warning(request,
                            _(u'The project "%(name)s" is %(state)s for %(lang)s auditory.') % params)

        super(Project, self).save(*args, **kwargs)

    @property
    def teaser(self):
        u"""Возвращает главное изображение проекта."""
        try:
            return ImageQueue.objects.get(teaser=True, tags=self.code)
        except ImageQueue.DoesNotExist:
            return None

    def is_ready_to_public(self, lang, fields=None):
        u"""
        Проверяет готовность проекта к публикации на сайте.

        Обязательные поля:
        * code - проверка на уровне БД;
        * customer - проверка на уровне БД;
        * address - проверка на уровне перевода;
        * short_name - проверка на уровне БД;
        * ptype - значение по умолчанию;
        * status - значение по умолчанию;
        * object_square - значение по умолчанию;
        * reg_date - проверка на уровне БД.

        Также обязательно наличие тизера, что подразумевает загрузку картинки.
        """
        if self.teaser is None:
            return False
        if fields is None:
            from .. translation import ProjectOpts as opts
            fields = opts.fields
        for field in fields:
            field_name = u'%s_%s' % (field, lang)
            value = getattr(self, field_name)
            if value is None or 0 == len(value.strip()):
                return False
        return True

    @property
    def price_meter(self):
        u"""Цена за квадратный метр."""
        try:
            return self.price_full / self.object_square
        except decimal.DivisionByZero:
            return 0

    @property
    def duration_full(self):
        u"""Полные трудозатраты, в часах."""
        return self.duration_production + self.duration_changes + self.duration_discussion + self.duration_other

    @property
    def production_percent(self):
        u"""Процент производственного времени."""
        try:
            return self.duration_production * 100 / self.duration_full
        except ZeroDivisionError:
            return 0

    @property
    def meters_per_hour(self):
        u"""Скорость проектирования, метров в час."""
        try:
            return self.object_square / self.duration_production
        except ZeroDivisionError:
            return 0

    @property
    def speed(self):
        u"""Скорость проекта, метров в день."""
        try:
            return self.object_square / self.duration_full
        except ZeroDivisionError:
            return 0

    @property
    def created(self):
        u"""Дата создания проекта."""
        return self.registered.date

    @staticmethod
    def code_factory(pk=None, code=None):
        try:
            if pk:
                customer = Customer.objects.get(pk=pk)
            elif code:
                customer = Customer.objects.get(code=code)
            else:
                return None
        except Customer.DoesNotExist:
            return None

        # получаем список кодов для всех проектов заказчика, выделяем из них
        # порядковые номера и превращаем их в список целых чисел.
        project_ids = map(
            lambda x: int(x[0][5:7]),
            Project.objects.filter(
                customer__code=customer.code,
                code__iregex=r'^[0-9]{4}A[0-9]{4}'
            ).values_list('code')
        )

        tpl = '{customer_code:0>4}A{project_number:0>2}{year:0>2}'
        context = dict(
            customer_code=customer.code,
            project_number=(max(project_ids) if 0 < len(project_ids) else 0) + 1,
            year=date.today().strftime('%y'))
        return tpl.format(**context)


STAFF_TYPE_PERSON = 1
STAFF_TYPE_COMPANY = 2
STAFF_TYPE_CHOICES = (
    (STAFF_TYPE_PERSON, _(u'Person')),
    (STAFF_TYPE_COMPANY, _('Company')))


class Staff(models.Model):
    u"""
    Базовая модель члена команды: Человек или компания.

    Поле which используется для быстрого определения типа объекта.
    """
    which = models.IntegerField(choices=STAFF_TYPE_CHOICES, verbose_name=_(u'Type'))
    phone = models.CharField(max_length=32, blank=True, null=True, verbose_name=_(u'Phone'))
    email = models.CharField(max_length=128, blank=True, null=True, verbose_name=_(u'E-mail'))
    address = models.CharField(max_length=256, blank=True, null=True, verbose_name=_(u'Address'))
    first_name = models.CharField(max_length=64, blank=True, null=True, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=64, blank=True, null=True, verbose_name=_('Last Name'))
    company = models.CharField(max_length=256, blank=True, null=True, verbose_name=_(u'Company'))
    site = models.URLField(blank=True, null=True, verbose_name=u'Site URL')

    class Meta:
        verbose_name = _(u'Staff')
        verbose_name_plural = _(u'Staff')

    def __unicode__(self):
        if self.which == STAFF_TYPE_PERSON:
            value = u'%s %s' % (self.first_name, self.last_name)
            if self.company and self.company != '':
                value = u'%s (%s)' % (value, self.company)
            return value
        elif self.which == STAFF_TYPE_COMPANY:
            return self.company
        else:
            return _(u'Unknown type of record.')

    def is_translated(self, lang):
        from .. translation import StaffOpts as opts
        for field in opts.fields:
            field_name = u'%s_%s' % (field, lang)
            value = getattr(self, field_name)
            if value is None or 0 == len(value.strip()):
                return False
        return True

    @property
    def url(self):
        if self.which == STAFF_TYPE_COMPANY:
            return self.site
        else:
            return None


class MembershipRole(models.Model):
    title = models.CharField(max_length=64, verbose_name=_(u'Title'))

    class Meta:
        verbose_name = _(u'Membership Role')
        verbose_name_plural = _(u'Membership Roles')

    def __unicode__(self):
        return self.title

    def is_translated(self, lang):
        from .. translation import MembershipRoleOpts as opts
        for field in opts.fields:
            field_name = u'%s_%s' % (field, lang)
            value = getattr(self, field_name)
            if value is None or 0 == len(value.strip()):
                return False
        return True


class Membership(models.Model):
    project = models.ForeignKey(Project, verbose_name=_(u'Project'))
    role = models.ForeignKey(MembershipRole, verbose_name=_(u'Role'))
    staff = models.ManyToManyField(Staff, verbose_name=_(u'User'))
    position = models.IntegerField(default=0, verbose_name=_(u'Position'))
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


class Teaser(models.Model):
    project = models.ForeignKey(Project, verbose_name=_(u'Project'))
    lang = models.CharField(max_length=2, choices=settings.LANGUAGES, verbose_name=_(u'Language'))
    position = models.IntegerField(verbose_name=_(u'Position'))
    visible = models.BooleanField(default=False, verbose_name=_(u'Visible'))

    class Meta:
        verbose_name = _(u'Teaser')
        verbose_name_plural = _(u'Teasers')
        ordering = ('position', )

    def __unicode__(self):
        return self.project.short_name


def register_teaser(sender, instance, created, **kwargs):
    u"""
    При создании проекта следует создавать записи для каждого языка
    в модели управления тизером.
    """
    if created:
        for lang, name in settings.LANGUAGES:
            params = dict(project=instance, lang=lang, position=-1, visible=False)
            Teaser(**params).save()
models.signals.post_save.connect(register_teaser, Project)
