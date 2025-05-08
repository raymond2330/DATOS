from django.contrib import admin
from .models import (
    User, ResearchPaper, Dataset, Request, Author, PaperAuthor, DatasetAuthor,
    Category, Keyword, PaperKeyword, DatasetKeyword, PermissionChangeLog
)

class PaperAuthorInline(admin.TabularInline):
    model = PaperAuthor
    extra = 1

class PaperKeywordInline(admin.TabularInline):
    model = PaperKeyword
    extra = 1

class ResearchPaperAdmin(admin.ModelAdmin):
    inlines = [PaperAuthorInline, PaperKeywordInline]
    list_display = ('title', 'journal', 'publication_date', 'access_setting', 'uploaded_by')
    search_fields = ('title', 'journal')
    list_filter = ('access_setting', 'publication_date')

try:
    admin.site.unregister(ResearchPaper)
except admin.sites.NotRegistered:
    pass

admin.site.register(ResearchPaper, ResearchPaperAdmin)

admin.site.register(User)
admin.site.register(Dataset)
admin.site.register(Request)
admin.site.register(Author)
admin.site.register(PaperAuthor)
admin.site.register(DatasetAuthor)
admin.site.register(Category)
admin.site.register(Keyword)
admin.site.register(DatasetKeyword)
admin.site.register(PermissionChangeLog)
