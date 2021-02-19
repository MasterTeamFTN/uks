from django.test import TestCase, Client
from django.urls import reverse
from ..models import Milestone
from django.contrib.auth.models import User
from app.projects.models import Project

PROJECT_ID = 1
NONEXISTENT_PROJECT_ID = 3211
NONEXISTENT_MILESTONE_ID = 333

class TestMilestoneViews(TestCase):
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

    # milestone list view
    def test_milestone_list_view(self):
        response = self.client.get(reverse('milestone-list', args=[PROJECT_ID]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/milestone/milestone_list.html')


    def test_milestone_list_view_nonexistent_project(self):
        response = self.client.get(reverse('milestone-list', args=[NONEXISTENT_PROJECT_ID]))
        self.assertEquals(response.status_code, 404)



    # milestone create view
    def test_milestone_create_view(self):
        self.client.force_login(self.user)

        milestoneTitle = 'New milestone title'
        description = "New description"
        response = self.client.post(reverse('milestone-create', args=[self.project.pk]), {
            'title': milestoneTitle,
            'description': description,
            "project": self.project})

        self.assertEquals(Milestone.objects.filter(title=milestoneTitle).count(), 1)

    def test_milestone_create_view_project_not_exists(self):
        self.client.force_login(self.user)

        milestoneTitle = 'New milestone title'
        description = "New description"
        response = self.client.post(reverse('milestone-create', args=[NONEXISTENT_PROJECT_ID]), {
            'title': milestoneTitle,
            'description': description,
            "project": self.project})

        self.assertEquals(Milestone.objects.filter(title=milestoneTitle).count(), 0)
        self.assertEquals(response.status_code, 404)

    def test_milestone_create_view_user_not_contributor(self):
        self.client.force_login(self.user_non_contributor)

        milestoneTitle = 'New milestone title'
        description = "New description"
        response = self.client.post(reverse('milestone-create', args=[self.project.pk]), {
            'title': milestoneTitle,
            'description': description,
            "project": self.project})

        self.assertEquals(response.status_code, 403)

    def test_milestone_create_view_unauthorized(self):
        milestoneTitle = 'New milestone title'
        description = "New description"
        response = self.client.post(reverse('milestone-create', args=[self.project.pk]), {
            'title': milestoneTitle,
            'description': description,
            "project": self.project})

        self.assertEquals(response.status_code, 302)



    # milestone delete
    def test_milestone_delete_view(self):
        self.client.force_login(self.user)

        milestoneTitle="generic-milestone"
        description = "New description"
        milestone = Milestone.objects.create(
            project=self.project,
            title=milestoneTitle,
            description= description
        )

        response = self.client.delete(reverse('milestone-delete', args=[self.project.pk, milestone.pk]))
        self.assertEquals(Milestone.objects.filter(title=milestoneTitle).count(), 0)
        self.assertEquals(response.status_code, 302)

    def test_milestone_delete_view_nonexistent(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse('milestone-delete', args=[self.project.pk, NONEXISTENT_MILESTONE_ID]))

        self.assertEquals(response.status_code, 404)

    # milestone update

    def test_milestone_update_view(self):
        self.client.force_login(self.user)

        milestone = Milestone.objects.create(
            project = self.project,
            title = "generic-milestone",
            description = "description"
        )

        response = self.client.post(reverse('milestone-update', args=[milestone.project.pk, milestone.pk]), {
            'title': milestone.title,
            'description': "new description"
            })

        self.assertEquals(response.status_code, 302)
        milestone.refresh_from_db()
        self.assertEquals(milestone.description, "new description")


    def test_milestone_update_view_nonexistent(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('milestone-update', args=[self.project.pk, NONEXISTENT_MILESTONE_ID]), {
            'name': "generic-milestone",
            'description': "new description"
            })
        self.assertEquals(response.status_code, 404)
