from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Milestone
from app.projects.models import Project
from app.organizations.models import Organization
from pyasn1.type.univ import Null
import datetime

MILESTONE_ID = 1

class TestMilestoneModels(TestCase):

    def setUp(self):
        user = User.objects.create(
            username='testuser'
        )

        proj = Project()
        proj.save()
        proj.name = "Test project";
        proj.description = "Test description";
        proj.is_public = True;
        proj.contributors.add(user);
        proj.save();

        Milestone.objects.create(
            project=proj,
            title="generic-milestone",
            description="create generic milestone"
        )

    def test(self):
        genericMilestone = Milestone.objects.get(title="generic-milestone")
        self.assertEquals(genericMilestone.description, "create generic milestone")
        self.assertEquals(genericMilestone.project.name, "Test project")
