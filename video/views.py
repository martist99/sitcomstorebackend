from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import generics,status
from .models import CATEGORY_CHOICES,Video,WatchLater,LikedVideo,History,Playlist,Comment
from .serializers import PlaylistSerializer,VideoSerializer,WatchLaterSerializer,HistorySerializer,LikedVideoSerializer,CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from account.authenticate import CustomAuthentication
from account.models import User
from account.serializer import UserSerializer
# Create your views here.

from django.shortcuts import get_object_or_404

@api_view(['GET'])
def category_choices(request):
    category_choices = [value for value,_  in CATEGORY_CHOICES]
    return Response({'categories': category_choices})

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['category', 'creator','title']

class VideoView(generics.RetrieveAPIView):
    serializer_class = VideoSerializer
    queryset=Video.objects.all()
        
class WatchLaterListByUserAPIView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes=([CustomAuthentication])

    def get_queryset(self):
        user = self.request.user
        watch_later_entries = WatchLater.objects.filter(user=user)
        videos = [watch_later.video for watch_later in watch_later_entries]
        return videos

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
class WatchLaterCreateAPIView(generics.CreateAPIView):
    serializer_class = WatchLaterSerializer
    permission_classes = [IsAuthenticated]  # Add appropriate permissions
    authentication_classes=([CustomAuthentication])

    def perform_create(self, serializer):
        
        request_user = self.request.user
        if 'user' in serializer.validated_data and serializer.validated_data['user'] != request_user:
            raise ValidationError({"error":"Not Authenticated user"},code=401)
        video_id = serializer.validated_data.get('video', None)  
        if video_id is not None and WatchLater.objects.filter(user=request_user, video=video_id).exists():
            raise ValidationError({'detail': 'This video is already in the watch later list.'},code=401)
         
        serializer.save(user=request_user)

class WatchLaterDeleteAPIView(generics.DestroyAPIView):
    queryset = WatchLater.objects.all()
    serializer_class = WatchLaterSerializer
    permission_classes = [IsAuthenticated]  # Add appropriate permissions
    authentication_classes=([CustomAuthentication])

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        video_id = self.kwargs['video_id']
        watch_later = get_object_or_404(WatchLater, user=user, video=video_id)

        # Check if the requesting user is the owner of the WatchLater object
        if watch_later.user != user:
            raise ValidationError({'detail': 'You do not have permission to perform this action.'},403)

        watch_later.delete()
        return Response({'detail': 'Successfully removed from watch later.'}, status=status.HTTP_204_NO_CONTENT)
    
#Liked Handler 
class LikedListByUserAPIView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes=([CustomAuthentication])

    def get_queryset(self):
        user = self.request.user
        liked_entries = LikedVideo.objects.filter(user=user)
        videos = [watch_later.video for watch_later in liked_entries]
        return videos

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
class LikedCreateAPIView(generics.CreateAPIView):
    serializer_class = LikedVideoSerializer
    permission_classes = [IsAuthenticated]  # Add appropriate permissions
    authentication_classes=([CustomAuthentication])

    def perform_create(self, serializer):
        
        request_user = self.request.user
        if 'user' in serializer.validated_data and serializer.validated_data['user'] != request_user:
            raise ValidationError({"error":"Not AUthenticated user"},code=401)
        video_id = serializer.validated_data.get('video', None)  
        if video_id is not None and LikedVideo.objects.filter(user=request_user, video=video_id).exists():
            raise ValidationError({'detail': 'This video is already liked.'},code=401)
        
        serializer.save(user=request_user)

class LikedDeleteAPIView(generics.DestroyAPIView):
    queryset = LikedVideo.objects.all()
    serializer_class = LikedVideoSerializer
    permission_classes = [IsAuthenticated]  # Add appropriate permissions
    authentication_classes=([CustomAuthentication])

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        video_id = self.kwargs['video_id']
        liked = get_object_or_404(LikedVideo, user=user, video=video_id)

        # Check if the requesting user is the owner of the WatchLater object
        if liked.user != user:
            raise ValidationError({'detail': 'You do not have permission to perform this action.'},403)

        liked.delete()
        return Response({'detail': 'Successfully removed from liked.'}, status=status.HTTP_204_NO_CONTENT)
    

#History Handler 
class HistoryListByUserAPIView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes=([CustomAuthentication])

    def get_queryset(self):
        user = self.request.user
        history_entries = History.objects.filter(user=user)
        videos = [history.video for history in history_entries]
        return videos

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
class HistoryCreateAPIView(generics.CreateAPIView):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]  # Add appropriate permissions
    authentication_classes=([CustomAuthentication])

    def perform_create(self, serializer):
        
        request_user = self.request.user
        if 'user' in serializer.validated_data and serializer.validated_data['user'] != request_user:
            raise ValidationError({"error":"Not AUthenticated user"},code=401)
        video_id = serializer.validated_data.get('video', None)  
        if video_id is not None and History.objects.filter(user=request_user, video=video_id).exists():
            raise ValidationError({'detail': 'This video is already liked.'},code=401)
        
        serializer.save(user=request_user)

class HistoryDeleteAPIView(generics.DestroyAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]  # Add appropriate permissions
    authentication_classes=([CustomAuthentication])

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        video_id = self.kwargs['video_id']
        history = get_object_or_404(History, user=user, video=video_id)

        # Check if the requesting user is the owner of the WatchLater object
        if history.user != user:
            raise ValidationError({'detail': 'You do not have permission to perform this action.'},403)

        history.delete()
        return Response({'detail': 'Successfully removed from History.'}, status=status.HTTP_204_NO_CONTENT)



class HistoryClearByUserAPIView(generics.DestroyAPIView):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes=([CustomAuthentication])

    def destroy(self, request, *args, **kwargs):
        user = self.request.user

        # Delete all history entries for the specified user
        History.objects.filter(user=user).delete()

        return Response({'detail': 'Successfully cleared history for the user.'}, status=status.HTTP_204_NO_CONTENT)
    
    
#Playliust handler 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def playlist_list_by_user(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

    user = request.user
    playlists = Playlist.objects.filter(user=user)
    
    # Customize the serializer to include details about the videos within each playlist
    serializer = PlaylistSerializer(playlists, many=True, context={'request': request})

    return Response(serializer.data)


class PlaylistCreateAPIView(generics.CreateAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes=([CustomAuthentication])

    def perform_create(self, serializer):
        # Set the user of the playlist to the authenticated user
        serializer.save(user=self.request.user)
        
        
class PlaylistDeleteAPIView(generics.DestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes=([CustomAuthentication])

    def get_object(self):
        user = self.request.user
        playlist_id = self.kwargs['playlist_id']
        return get_object_or_404(Playlist, user=user, id=playlist_id)

    def destroy(self, request, *args, **kwargs):
        playlist = self.get_object()

        # Check if the requesting user is the owner of the playlist
        if playlist.user != request.user:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        playlist.delete()
        return Response({'detail': 'Playlist successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])

def playlist_videos(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except Playlist.DoesNotExist:
        return Response({'detail': 'Playlist not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the requesting user is the owner of the playlist
    if playlist.user != request.user:
        return Response({'detail': 'You do not have permission to view this playlist.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = PlaylistSerializer(playlist)
    return Response(serializer.data['videos'])


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def add_video_to_playlist(request, playlist_id, video_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except Playlist.DoesNotExist:
        return Response({'detail': 'Playlist not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the requesting user is the owner of the playlist
    if playlist.user != request.user:
        return Response({'detail': 'You do not have permission to modify this playlist.'}, status=status.HTTP_403_FORBIDDEN)

    if playlist.videos.filter(id=video_id).exists():
        return Response({'detail': 'This video is already in the playlist.'}, status=status.HTTP_400_BAD_REQUEST)
    # Assume Video model has a ForeignKey to Playlist model, adjust as needed
    playlist.videos.add(video_id)
    playlist.save()

    serializer = PlaylistSerializer(playlist)
    return Response({"detail":"successfully added to playlist"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def remove_video_from_playlist(request, playlist_id, video_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except Playlist.DoesNotExist:
        return Response({'detail': 'Playlist not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the requesting user is the owner of the playlist
    if playlist.user != request.user:
        return Response({'detail': 'You do not have permission to modify this playlist.'}, status=status.HTTP_403_FORBIDDEN)

    if not playlist.videos.filter(id=video_id).exists():
        return Response({'detail': 'This video is not in the playlist.'}, status=status.HTTP_400_BAD_REQUEST)
    # Assume Video model has a ForeignKey to Playlist model, adjust as needed
    playlist.videos.remove(video_id)
    playlist.save()

    serializer = Playlist(playlist)
    return Response({"detail":"successfully deleted"}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def video_presence_in_playlists(request, video_id):
    try:
        # Get the video by ID
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return Response({'detail': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)
    user=request.user
    playlists = Playlist.objects.filter(user=user)

    # Create a list of dictionaries with playlist name and boolean indicating video presence
    playlist_data = []
    for playlist in playlists:
        is_video_present = playlist.videos.filter(id=video_id).exists()
        playlist_info = {
            'playlist_name': playlist.title,
            'id':playlist.id,
            'is_video_present': is_video_present,
        }
        playlist_data.append(playlist_info)

    return Response(playlist_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def is_video_liked(request, video_id):
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return Response({'detail': 'Video not found.'}, status=404)

    user = request.user
    is_liked = LikedVideo.objects.filter(user=user, video=video).exists()

    return Response({'is_liked': is_liked}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])

def is_video_in_watch_later(request, video_id):
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return Response({'detail': 'Video not found.'}, status=404)

    user = request.user
    is_in_watch_later = WatchLater.objects.filter(user=user, video=video).exists()

    return Response({'is_in_watch_later': is_in_watch_later}, status=200)




class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        video_id = request.data.get('video', None)
        parent_comment_id = request.data.get('parent_comment', None)

        # Check if the parent comment belongs to the same video
        if parent_comment_id:
            parent_comment = Comment.objects.filter(id=parent_comment_id, video_id=video_id)

            if not parent_comment.exists():
                return Response({"error": "Parent comment does not belong to the same video."},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

@api_view(['GET'])
def nested_comments_by_video(request, video_id):
    top_level_comments = Comment.objects.filter(video_id=video_id, parent_comment=None).order_by('-created_at')
    serialized_comments = CommentSerializer(top_level_comments, many=True).data
    
    for comment in serialized_comments:
        user_id= comment['user']   # Assuming user_id is present in the serialized data
        user_data = User.objects.get(id=user_id)  # Replace YourUserModel with your actual user model
        user_serializer = UserSerializer(user_data)  # Replace YourUserSerializer with your actual user serializer
        comment['user'] = user_serializer.data
        comment['replies'] = CommentSerializer(
            Comment.objects.filter(parent_comment_id=comment['id']).order_by('-created_at'),
            many=True
        ).data

    return Response(serialized_comments)