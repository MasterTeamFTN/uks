from django.test import TestCase, Client
from django.urls import reverse
from ..models import Label
from django.contrib.auth.models import User
from app.projects.models import Project

PROJECT_ID = 1
NONEXISTENT_PROJECT_ID = 5265
NONEXISTENT_LABEL_ID = 1991

class TestLabelViews(TestCase):
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
        

    ### Tests about label LIST VIEW
    ############################
    def test_labels_list_view(self):
        response = self.client.get(reverse('label-list', args=[PROJECT_ID]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/label/label_list.html')

    
    def test_labels_list_view_nonexistent_project(self):
        response = self.client.get(reverse('label-list', args=[NONEXISTENT_PROJECT_ID]))
        self.assertEquals(response.status_code, 404)



    ### Tests about label CREATE
    ############################
    def test_label_create_view(self):
        self.client.force_login(self.user)

        labelName = 'New label name'
        description = "New description"
        response = self.client.post(reverse('label-create', args=[self.project.pk]), {
            'name': labelName,
            'color': "#FF0000",
            'description': description,
            "project": self.project})

        # lastLab = Label.objects.get(name=labelName)

        self.assertEquals(Label.objects.last().name, labelName)
        
    def test_label_create_view_unauthorized(self):
        labelName = 'New label name'
        response = self.client.post(reverse('label-create', args=[self.project.pk]), {
            'name': labelName,
            'color': "#FF0000",
            'description': "New description",
            "project": self.project})


        self.assertEquals(response.status_code, 302)
        self.assertEquals(Label.objects.filter(name=labelName).count(), 0)

    def test_label_create_view_project_not_exists(self):
        self.client.force_login(self.user)

        labelName = 'New label name'
        response = self.client.post(reverse('label-create', args=[NONEXISTENT_PROJECT_ID]), {
            'name': labelName,
            'color': "#FF0000",
            'description': "New description",
            "project": self.project})

        self.assertEquals(response.status_code, 404)
        self.assertEquals(Label.objects.filter(name=labelName).count(), 0)
        
    def test_label_create_view_user_not_contributor(self):
        self.client.force_login(self.user_non_contributor)

        labelName = 'New label name'
        response = self.client.post(reverse('label-create', args=[self.project.pk]), {
            'name': labelName,
            'color': "#FF0000",
            'description': "New description",
            "project": self.project})
        
        self.assertEquals(response.status_code, 403)
        self.assertEquals(Label.objects.filter(name=labelName).count(), 0)




    ### Tests about label DELETE
    ############################
    def test_label_delete_view(self):
        self.client.force_login(self.user)
        
        labelName="generic-feature-label"
        label = Label.objects.create( 
            project=self.project,
            name=labelName,
            color="#000000",
            description="create generic form"
        )
        
        response = self.client.delete(reverse('label-delete', args=[label.project.pk, label.pk]))
        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Label.objects.filter(name=labelName).count(), 0)

        
    def test_label_delete_view_user_not_contributor(self):
        self.client.force_login(self.user_non_contributor)

        labelName="generic-feature-label"
        label = Label.objects.create( 
            project=self.project,
            name=labelName,
            color="#000000",
            description="create generic form"
        )

        response = self.client.delete(reverse('label-delete', args=[label.project.pk, label.pk]))
        
        self.assertEquals(response.status_code, 403)
        self.assertEquals(Label.objects.filter(name=labelName).count(), 1)
        label.delete() # Cleanup
    
    def test_label_delete_view_label_nonexistent(self):
        self.client.force_login(self.user)
        labelName="generic-feature-label"
        label = Label.objects.create( 
            project=self.project,
            name=labelName,
            color="#000000",
            description="create generic form"
        )

        response = self.client.delete(reverse('label-delete', args=[label.project.pk, NONEXISTENT_LABEL_ID]))
        
        self.assertEquals(response.status_code, 404)
        label.delete() # Cleanup


    ### Tests about label UPDATE
    ############################
    def test_label_update_view(self):
        self.client.force_login(self.user)

        label = Label.objects.create( 
            project = self.project,
            name = "generic-feature-label",
            color ="#000000",
            description = "description"
        )

        response = self.client.post(reverse('label-update', args=[label.project.pk, label.pk]), {
            'name': label.name,
            'color': "#000000",
            'description': "new description"
            })

        self.assertEquals(response.status_code, 302)
        label.refresh_from_db()
        self.assertEquals(label.description, "new description")

        
    def test_label_update_view_user_not_contributor(self):
        self.client.force_login(self.user_non_contributor)

        labelName = 'generic-feature-label'
        label = Label.objects.create( 
            project = self.project,
            name = labelName,
            color ="#000000",
            description = "description"
        )

        response = self.client.post(reverse('label-update', args=[label.project.pk, label.pk]), {
            'name': labelName,
            'color': "#000000",
            'description': "new description"
            })

        self.assertEquals(response.status_code, 403)
        self.assertEquals(Label.objects.filter(name=labelName).count(), 1)
        label.delete() # Cleanup


    def test_label_update_view_label_nonexistent(self):
        self.client.force_login(self.user)
        labelName="generic-feature-label"

        response = self.client.post(reverse('label-update', args=[self.project.pk, NONEXISTENT_LABEL_ID]), {
            'name': labelName,
            'color': "#000000",
            'description': "new description"
            })
        self.assertEquals(response.status_code, 404)
        
    def test_label_update_view_project_nonexistent(self):
        self.client.force_login(self.user)
        labelName="generic-feature-label"

        labelName = 'generic-feature-label'
        label = Label.objects.create( 
            project = self.project,
            name = labelName,
            color ="#000000",
            description = "description"
        )

        with self.assertRaises(Project.DoesNotExist):
            response = self.client.post(reverse('label-update', args=[NONEXISTENT_PROJECT_ID, label.pk]), {
                'name': labelName,
                'color': "#000000",
                'description': "new description"
                })
            self.assertEquals(response.status_code, 404)