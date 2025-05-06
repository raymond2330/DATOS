from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import (
    ResearchPaper, Dataset, Category, Request, Author, PaperAuthor, DatasetAuthor,
    Keyword, PaperKeyword, DatasetKeyword, PermissionChangeLog
)
from faker import Faker

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate dummy data for all models in the database'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create categories
        categories = [Category.objects.create(name=fake.word()) for _ in range(5)]

        # Create users
        roles = ['guest', 'student', 'admin']
        users = [
            User.objects.create_user(
                username=fake.user_name(),
                password='password123',
                role=role
            ) for role in roles
        ]

        # Create authors
        authors = [
            Author.objects.create(name=fake.name(), affiliation=fake.company())
            for _ in range(10)
        ]

        # Create research papers and datasets
        for _ in range(10):
            paper = ResearchPaper.objects.create(
                title=fake.sentence(),
                abstract=fake.text(),
                journal=fake.company(),
                publication_details=fake.text(),
                access_setting='open',
                file_url=fake.url(),
                preview_url=fake.url(),
                uploaded_by=fake.random_element(users),
                category=fake.random_element(categories)
            )

            dataset = Dataset.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                version=fake.random_number(digits=1),
                size=fake.random_number(digits=2),
                file_url=fake.url(),
                preview_url=fake.url(),
                access_setting='open',
                uploaded_by=fake.random_element(users)
            )

            # Link authors to papers and datasets
            for author in fake.random_elements(authors, length=3):
                PaperAuthor.objects.create(paper=paper, author=author)
                DatasetAuthor.objects.create(dataset=dataset, author=author)

        # Create keywords and link them to papers and datasets
        keywords = [Keyword.objects.create(term=fake.word()) for _ in range(10)]
        for paper in ResearchPaper.objects.all():
            for keyword in fake.random_elements(keywords, length=3):
                PaperKeyword.objects.create(paper=paper, keyword=keyword)

        for dataset in Dataset.objects.all():
            for keyword in fake.random_elements(keywords, length=3):
                DatasetKeyword.objects.create(dataset=dataset, keyword=keyword)

        # Create requests
        for _ in range(10):
            Request.objects.create(
                user=fake.random_element(users),
                paper=fake.random_element(ResearchPaper.objects.all()),
                dataset=fake.random_element(Dataset.objects.all()),
                purpose=fake.sentence(),
                reason_for_access=fake.text(),
                status=fake.random_element(['pending', 'approved', 'rejected'])
            )

        # Create permission change logs
        for _ in range(5):
            PermissionChangeLog.objects.create(
                request=fake.random_element(Request.objects.all()),
                admin=fake.random_element([user for user in users if user.role == 'admin']),
                action=fake.random_element(['approved', 'rejected'])
            )

        self.stdout.write(self.style.SUCCESS('Dummy data for all models generated successfully!'))