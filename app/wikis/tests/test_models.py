from django.test import TestCase, Client
from django.contrib.auth.models import User
from ..models import Wiki, WikiVersion
from ...projects.models import Project

WIKI_PAGE_NAME = 'Wiki home page'

class TestWikiModels(TestCase):
    pass

    # TODO: Implement this
    # TODO: Treba naci nacin kako mockovati save metodu ili kako proslediti autentifikovanog user-a
    # def setUp(self):
    #     self.project = Project.objects.create(
    #         name='UKS Lab',
    #         description='This is project description',
    #         github_url='' # we don't need branches and commits here
    #     )

    #     self.wiki = Wiki.objects.create(title=WIKI_PAGE_NAME, project=self.project)

    # def test_str(self):
    #     self.assertEquals(self.wiki.__str__(), WIKI_PAGE_NAME)
        

