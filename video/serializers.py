from rest_framework import serializers
from .models import Video,WatchLater,LikedVideo,History,Playlist,Comment
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Video
        fields='__all__'

class WatchLaterSerializer(serializers.ModelSerializer):
    class Meta:
        model=WatchLater
        fields='__all__'

class LikedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=LikedVideo
        fields='__all__'

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=History
        fields='__all__'
        
class PlaylistSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    class Meta:
        model=Playlist
        fields = ['id', 'user', 'title', 'videos', 'created_at']
        read_only_fields = ['user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'video', 'text', 'created_at', 'parent_comment']