from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import MilestoneCreateView, milestone_detail_view, MilestoneDeleteView, milestone_list_view, MilestoneUpdateView

PROJECT_ID = 1
MILESTONE_ID = 1

class TestMilestoneUrls(SimpleTestCase):

    def test_milestone_create(self):
        url = reverse('milestone-create', args=[PROJECT_ID])
        self.assertEquals(resolve(url).func.view_class, MilestoneCreateView)

    def test_milestone_detail(self):
        url = reverse('milestone-detail', args=[PROJECT_ID, MILESTONE_ID])
        self.assertEquals(resolve(url).func, milestone_detail_view)

    def test_milestone_delete(self):
        url = reverse('milestone-delete', args=[PROJECT_ID, MILESTONE_ID])
        self.assertEquals(resolve(url).func.view_class, MilestoneDeleteView)

    def test_milestone_list(self):
        url = reverse('milestone-list', args=[PROJECT_ID])
        self.assertEquals(resolve(url).func, milestone_list_view)

    def test_milestone_update(self):
        url = reverse('milestone-update', args=[PROJECT_ID, MILESTONE_ID])
        self.assertEquals(resolve(url).func.view_class, MilestoneUpdateView)
