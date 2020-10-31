from django.contrib import admin

from .models import Post, PhotoMedia, LinkMedia

admin.site.register(Post)
admin.site.register(PhotoMedia)
admin.site.register(LinkMedia)
