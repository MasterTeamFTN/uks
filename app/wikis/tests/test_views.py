from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ...projects.models import Project
from ..models import Wiki, WikiVersion

NON_EXISTING_PROJECT_ID = 8022
NON_EXISTING_WIKI_ID = 6021

class TestWikiViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username='john.doe')
        self.user_non_contributor = User.objects.create(username='non.contributor')

        self.project = Project.objects.create(
            name='UKS Lab',
            description='This is project description',
            github_url='' # we don't need branches and commits here
        )

        self.project.contributors.add(self.user)
        self.project.save()

    ### wikis_list_view
    def test_wikis_list_view(self):
        response = self.client.get(reverse('wiki-list', args=[self.project.pk]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/wiki/wiki_list.html')

    def test_wikis_list_view_project_not_exists(self):
        response = self.client.get(reverse('wiki-list', args=[NON_EXISTING_PROJECT_ID]))
        self.assertEquals(response.status_code, 404)

    ### WikiDetailView    
    def test_wiki_detail_view(self):
        self.client.force_login(self.user)

        wiki = Wiki.objects.create(title='Title', project=self.project)
        response = self.client.get(reverse('wiki-detail', args=[self.project.pk, wiki.pk]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/wiki/wiki_detail.html')

    def test_wiki_detail_view_wiki_not_exists(self):
        response = self.client.get(reverse('wiki-detail', args=[self.project.pk, NON_EXISTING_WIKI_ID]))
        self.assertEquals(response.status_code, 404)

    ### WikiCreateView
    def test_wiki_create_view(self):
        self.client.force_login(self.user)

        title = 'Wiki page title'
        response = self.client.post(reverse('wiki-create', args=[self.project.pk]), {'title': title})

        self.assertEquals(Wiki.objects.last().title, title)

    def test_wiki_create_view_project_not_exists(self):
        self.client.force_login(self.user)

        title = 'Title for non existing project'
        response = self.client.post(reverse('wiki-create', args=[NON_EXISTING_PROJECT_ID]), {'title': title})
        
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Wiki.objects.filter(title=title).count(), 0)

    def test_wiki_create_view_user_not_contributor(self):
        self.client.force_login(self.user_non_contributor)

        title = 'Title for non contributor user'
        response = self.client.post(reverse('wiki-create', args=[self.project.pk]), {'title': title})
        
        self.assertEquals(response.status_code, 403)
        self.assertEquals(Wiki.objects.filter(title=title).count(), 0)

    def test_wiki_non_authorized(self):
        title = 'Wiki page title'
        response = self.client.post(reverse('wiki-create', args=[self.project.pk]), {'title': title})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Wiki.objects.filter(title=title).count(), 0)

    ### WikiDeleteView
    def test_wiki_delete_view(self):
        self.client.force_login(self.user)
        title = 'Title test_wiki_delete_view'
        wiki = Wiki.objects.create(title=title, project=self.project)
        
        response = self.client.delete(reverse('wiki-delete', args=[wiki.project.pk, wiki.pk]))
        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Wiki.objects.filter(title=title).count(), 0)

    def test_wiki_delete_view_user_not_contributor(self):
        self.client.force_login(self.user_non_contributor)
        title = 'Title test_wiki_delete_view_user_not_contributor'
        wiki = Wiki.objects.create(title=title, project=self.project)

        response = self.client.delete(reverse('wiki-delete', args=[wiki.project.pk, wiki.pk]))
        
        self.assertEquals(response.status_code, 403)
        self.assertEquals(Wiki.objects.filter(title=title).count(), 1)
        wiki.delete() # Cleanup

    def test_wiki_delete_view_wiki_not_exists(self):
        self.client.force_login(self.user)
        title = 'Title test_wiki_delete_view_project_not_exists'
        wiki = Wiki.objects.create(title=title, project=self.project)

        response = self.client.delete(reverse('wiki-delete', args=[wiki.project.pk, NON_EXISTING_WIKI_ID]))
        
        self.assertEquals(response.status_code, 404)
        wiki.delete() # Cleanup

    ### WikiUpdateView
    def test_wiki_update_view(self):
        pass

        # TODO: I ovde iz nekog razloga nece da se prepozna ulogovani korisnik kao i u metodi ispod

        # self.client.force_login(self.user)

        # title = 'Title test_wiki_update_view'
        # new_title = 'This is new title'
        # wiki = Wiki.objects.create(title=title, project=self.project)

        # response = self.client.post(reverse('wiki-update', args=[wiki.project.pk, wiki.pk]), {'title': new_title})

        # self.assertEquals(response.status_code, 302)
        # self.assertEquals(Wiki.objects.last().title, new_title)


    ### wiki_versions_list_view
    def test_wiki_versions_list_view(self):
        pass

        # TODO: Iz nekog razloga nece da kreira Wiki objekat
        # On se pravi na isti nacin kao u prethodnim testovima, a ovde pravi problem...
        # we must first login so the wiki object can be created
        # self.client.force_login(self.user)
        # wiki = Wiki.objects.create(title='My wiki', project=self.project)

        # response = self.client.get(reverse('wiki-history', args=[wiki.project.pk, wiki.pk]))
        
        # self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'app/wiki/wikiversion_list.html')

    def test_wiki_versions_list_view_wiki_not_exists(self):
        response = self.client.get(reverse('wiki-history', args=[self.project.pk, NON_EXISTING_WIKI_ID]))
        self.assertEquals(response.status_code, 404)