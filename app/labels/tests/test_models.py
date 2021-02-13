from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Label
from app.projects.models import Project
from app.organizations.models import Organization
from pyasn1.type.univ import Null
import datetime

PROJECT_ID = 1 

class TestLabelModels(TestCase):

    def setUp(self):
        user = User.objects.create(
            username='testuser'
        )

        proj = Project()
        proj.save()
        proj.name = "Test project";
        proj.description = "Test description";
        # proj.created_on = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ");
        # proj.github_url = "https://github.com/LjubicJanko/LiveHealthy";
        # proj.updated_on = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ");
        proj.is_public = True;
        proj.contributors.add(user);
        proj.save();

        Label.objects.create( 
            project=proj,
            name="generic-feature-label",
            color="#000000",
            description="create generic form"
        )

    def test(self):
        genericFeatureLabel = Label.objects.get(name="generic-feature-label")
        self.assertEquals(genericFeatureLabel.color, "#000000")
        self.assertEquals(genericFeatureLabel.project.name, "Test project")