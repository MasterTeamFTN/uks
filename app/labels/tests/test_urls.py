from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import LabelUpdateView, LabelDeleteView, LabelCreateView, label_list_view

PROJECT_ID = 1
LABEL_ID = 1

class TestLabelUrls(SimpleTestCase):

     def test_label_list(self):
        url = reverse('label-list', args=[PROJECT_ID])
        self.assertEquals(resolve(url).func, label_list_view)

     def test_label_create_view(self):
        url = reverse('label-create', args=[PROJECT_ID])
        self.assertEquals(resolve(url).func.view_class, LabelCreateView)

     def test_label_update_view(self):
        url = reverse('label-update', args=[PROJECT_ID, LABEL_ID])
        self.assertEquals(resolve(url).func.view_class, LabelUpdateView)

     def test_label_delete(self):
        url = reverse('label-delete', args=[PROJECT_ID, LABEL_ID])
        self.assertEquals(resolve(url).func.view_class, LabelDeleteView)
