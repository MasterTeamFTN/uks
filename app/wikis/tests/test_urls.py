from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import wikis_list_view, WikiDetailView, WikiCreateView, WikiDeleteView, WikiUpdateView, wiki_versions_list_view

PROJECT_ID = 1
WIKI_ID = 1

class TestWikiUrls(SimpleTestCase):

    def test_wiki_list(self):
        url = reverse('wiki-list', args=[PROJECT_ID])
        self.assertEquals(resolve(url).func, wikis_list_view)

    def test_wiki_create(self):
        url = reverse('wiki-create', args=[PROJECT_ID])
        self.assertEquals(resolve(url).func.view_class, WikiCreateView)

    def test_wiki_detail(self):
        url = reverse('wiki-detail', args=[PROJECT_ID, WIKI_ID])
        self.assertEquals(resolve(url).func.view_class, WikiDetailView)

    def test_wiki_delete(self):
        url = reverse('wiki-delete', args=[PROJECT_ID, WIKI_ID])
        self.assertEquals(resolve(url).func.view_class, WikiDeleteView)

    def test_wiki_update(self):
        url = reverse('wiki-update', args=[PROJECT_ID, WIKI_ID])
        self.assertEquals(resolve(url).func.view_class, WikiUpdateView)

    def test_wiki_history(self):
        url = reverse('wiki-history', args=[PROJECT_ID, WIKI_ID])
        self.assertEquals(resolve(url).func, wiki_versions_list_view)
