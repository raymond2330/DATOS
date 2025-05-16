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

class DatasetAuthorInline(admin.TabularInline):
    model = DatasetAuthor
    extra = 1

class DatasetKeywordInline(admin.TabularInline):
    model = DatasetKeyword
    extra = 1

class DatasetAdmin(admin.ModelAdmin):
    inlines = [DatasetAuthorInline, DatasetKeywordInline]
    list_display = ('title', 'version', 'size', 'access_setting', 'uploaded_by')
    search_fields = ('title', 'version')
    list_filter = ('access_setting',)

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'paper', 'dataset', 'purpose', 'status', 'request_date')
    search_fields = ('user__username', 'purpose')
    list_filter = ('status', 'request_date')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class KeywordAdmin(admin.ModelAdmin):
    list_display = ('term',)
    search_fields = ('term',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class DatasetAuthorAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'author')
    search_fields = ('dataset__title', 'author__name')

class DatasetKeywordAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'keyword')
    search_fields = ('dataset__title', 'keyword__term')

class PaperAuthorAdmin(admin.ModelAdmin):
    list_display = ('paper', 'author')
    search_fields = ('paper__title', 'author__name')

class PaperKeywordAdmin(admin.ModelAdmin):
    list_display = ('paper', 'keyword')
    search_fields = ('paper__title', 'keyword__term')

try:
    admin.site.unregister(ResearchPaper)
except admin.sites.NotRegistered:
    pass

admin.site.register(ResearchPaper, ResearchPaperAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(User)
admin.site.register(DatasetAuthor, DatasetAuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(DatasetKeyword, DatasetKeywordAdmin)
admin.site.register(PermissionChangeLog)
admin.site.register(PaperAuthor, PaperAuthorAdmin)
admin.site.register(PaperKeyword, PaperKeywordAdmin)
