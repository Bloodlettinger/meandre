# -*- coding: utf-8 -*-

from os.path import join, dirname, basename
from imghdr import what as mimetype

from django.core import management
from django.core.files.base import ContentFile

from django_webtest import WebTest
import factory
from haystack.query import SearchQuerySet

from ... test_settings import *
from ... uploader.models import Queue
from ... storage.models import Customer, Project
from ... users.models import CustomUser

__all__ = ('SearchTest', )


class UserFactory(factory.Factory):
    FACTORY_FOR = CustomUser


class CustomerFactory(factory.Factory):
    FACTORY_FOR = Customer

    customer_type = 1  # primary
    partnership_type = 1  # internal
    code = factory.Sequence(lambda n: '{0:04}'.format(int(n)))


class ProjectFactory(factory.Factory):
    FACTORY_FOR = Project

    customer = factory.LazyAttribute(lambda x: CustomerFactory())
    is_public_ru = True
    is_public_en = True
    price_full = 0
    exchange_rate = 0
    productivity = 0
    price_average = 0


POTENTIAL = 1
WINNED = 2


class SearchTest(WebTest):

    def setUp(self):
        self.user = UserFactory()
        self.projects = (
            ProjectFactory(short_name='one two three', status=WINNED),
            ProjectFactory(short_name='raz one tri', status=POTENTIAL)
        )

    def _add_image(self, project, full_path):
        content = ContentFile(open(full_path, 'r').read())
        file_name = basename(full_path)
        obj = Queue(
            uploaded_by=self.user,
            file_name=file_name,
            file_size=content.size,
            file_type=mimetype(full_path)
            )
        obj.tags = project.code
        obj.position = 0
        obj.image.save(file_name, content, save=True)

    def _rebuild_index(self):
        print  # чтобы вывод rebuild_index смотрелся нормально
        management.call_command('rebuild_index', interactive=False)

    def test_search_user(self):
        project_a, project_b = self.projects
        file_name = join(dirname(__file__), '..', '..', '..', 'tests', 'media', 'avatar.jpeg')
        self._add_image(project_a, file_name)

        self._rebuild_index()

        sqs = SearchQuerySet().filter(description='one')
        projects = Project.objects.filter(pk__in=[i.pk for i in sqs])
        self.assertEqual(2, projects.count())
        self.assertEqual(1, projects.winned().public().count())
