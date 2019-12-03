from django.contrib import admin
from .models import Post


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'publishing_date', 'slug']
    list_display_links = ['publishing_date']
    list_filter = ['publishing_date', 'title']
    search_fields = ['title', 'content']
    list_editable = ['title']

    # prepopulated_fields = {'slug': ('title',)} # admin panelinde post oluştururken slug kısmını title ile eş değer girer [editable=False yapıldığı için modelde burayı iptal ediyoruz.]

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)
