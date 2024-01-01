from django.db import models
from account.models import User
CATEGORY_CHOICES = (('all', 'all'),
                    ('the office', 'the office'),
                    ('friends', 'friends'),
                    ('suits', 'suits'))

# Create your models here.
class Video(models.Model):
    title=models.CharField(max_length=500)
    creator=models.CharField(max_length=500)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=500)
    logo=models.CharField(max_length=500)
    image=models.CharField(max_length=500)
    url=models.CharField(unique=True,max_length=500)
    def __str__(self) -> str:
        return self.title
    
class WatchLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.video.title} (Watch Later)"

class LikedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.video.title} (Liked)"

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.video.title} (Watched)"
    
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    videos = models.ManyToManyField(Video, related_name='playlists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.title} (Playlist)"