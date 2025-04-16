from django.contrib import admin
from .models import (
    User, ResearchPaper, Dataset, Request, Author, PaperAuthor, DatasetAuthor,
    Category, Keyword, PaperKeyword, DatasetKeyword, PermissionChangeLog
)

admin.site.register(User)
admin.site.register(ResearchPaper)
admin.site.register(Dataset)
admin.site.register(Request)
admin.site.register(Author)
admin.site.register(PaperAuthor)
admin.site.register(DatasetAuthor)
admin.site.register(Category)
admin.site.register(Keyword)
admin.site.register(PaperKeyword)
admin.site.register(DatasetKeyword)
admin.site.register(PermissionChangeLog)
