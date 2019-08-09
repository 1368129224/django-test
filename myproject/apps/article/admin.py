from django.contrib import admin
from .models import ArticleColumn

# Register your models here.
class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column', 'created', 'user')
    list_filter = ('column', 'user__username')
    search_fields = ('user__username', )

admin.site.register(ArticleColumn, ArticleColumnAdmin)