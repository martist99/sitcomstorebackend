from django.contrib import admin
from .models import Video,LikedVideo,WatchLater,History,Playlist
# Register your models here.
admin.site.register(Video)
admin.site.register(LikedVideo)
admin.site.register(WatchLater)
admin.site.register(History)
admin.site.register(Playlist)
