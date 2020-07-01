from rest_framework import serializers

from .models import Post, PhotoMedia, LinkMedia

class PhotoMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoMedia
        fields = '__all__'

class LinkMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkMedia
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    photo = PhotoMediaSerializer()
    link = LinkMediaSerializer()

    class Meta:
        model = Post
        fields = '__all__'
