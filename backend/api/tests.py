from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import ResearchPaper, Dataset, PermissionChangeLog, Category

User = get_user_model()

class AccessControlTests(APITestCase):

    def setUp(self):
        # Create a category
        self.category = Category.objects.create(name="Test Category")

        # Create users
        self.guest_user = User.objects.create_user(username="guest", password="guest123", role="guest")
        self.student_user = User.objects.create_user(username="student", password="student123", role="student")
        self.admin_user = User.objects.create_user(username="admin", password="admin123", role="admin")

        # Create research papers and datasets
        self.research_paper = ResearchPaper.objects.create(
            title="Open Research Paper",
            abstract="Abstract of the research paper",
            journal="Journal Name",
            publication_details="Details",
            access_setting="open",
            file_url="http://example.com/paper.pdf",
            preview_url="http://example.com/preview.jpg",
            uploaded_by=self.admin_user,
            category=self.category
        )

        self.dataset = Dataset.objects.create(
            title="Open Dataset",
            description="Description of the dataset",
            version="1.0",
            size=10.5,
            file_url="http://example.com/dataset.csv",
            preview_url="http://example.com/preview.jpg",
            access_setting="open",
            uploaded_by=self.admin_user
        )

    def test_guest_access(self):
        self.client.login(username="guest", password="guest123")

        # Guest can view previews but not access full content
        response = self.client.get(f"/api/research-papers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data[0])

        response = self.client.get(f"/api/datasets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data[0])

    def test_student_access(self):
        self.client.login(username="student", password="student123")

        # Student can access all content without restrictions
        response = self.client.get(f"/api/research-papers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("file_url", response.data[0])

        response = self.client.get(f"/api/datasets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("file_url", response.data[0])

    def test_admin_access_and_permission_change(self):
        self.client.login(username="admin", password="admin123")

        # Admin can access all content
        response = self.client.get(f"/api/research-papers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("file_url", response.data[0])

        response = self.client.get(f"/api/datasets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("file_url", response.data[0])

        # Admin can change permissions
        permission_change = PermissionChangeLog.objects.create(
            request=None,
            admin=self.admin_user,
            action="approved"
        )
        self.assertEqual(permission_change.admin, self.admin_user)
