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

class CreatorProfileField(serializers.Field):
    def to_representation(self, value):
        return (value.user.username, value.profile_picture)

class DateField(serializers.Field):
    def to_representation(self, value):
        return value.strftime("%b %-d, %Y")

class PostSerializer(serializers.ModelSerializer):
    photo = PhotoMediaSerializer()
    link = LinkMediaSerializer()
    profile = CreatorProfileField()
    date = DateField()

    class Meta:
        model = Post
        exclude = ['id', 'group']
