from rest_framework.serializers import( ModelSerializer,HyperlinkedIdentityField,SerializerMethodField)

from blog.models import Post
from comments.api.serializers import CommentCreateSerializer
from comments.models import Comments

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
            model=Post
            fields=[
                 #"id",
                "title",
                "content",
                "published",
                
               
            ]

class PostListSerializer(ModelSerializer):
    url=HyperlinkedIdentityField(
        view_name='postDetaillist',
        lookup_field='pk',
    )
    user=SerializerMethodField()
    class Meta:
            model=Post
            fields=[
                "url",
                "user",
                 "id",
                "title",
                "published",
                "content",  ]

    def get_user(self,obj):
        return str(obj.user.username)
    
post_delete_url=HyperlinkedIdentityField(
view_name='BlogPostDelete',
lookup_field='pk',)
    


class PostDetailSerializer(ModelSerializer):
    url=post_delete_url
    user=SerializerMethodField()
    image=SerializerMethodField()
    html=SerializerMethodField()
    comments=SerializerMethodField()
    
    class Meta:
            model=Post
            fields=[
                "url",
                "id",
                "user",
                "title",
                "published",
                "content",
                "html",
                "image",
                "comments",
                
            ]
    def get_user(self,obj):
        return str(obj.user.username)

    def get_html(self,obj):
        return obj.get_markdown()


    def get_image(self,obj):
        try:
            image=obj.image.url
        except:
            image=None
        return image

    def get_comments(self,obj):
        object_id=obj.id
        comments_qs=Comments.objects.filter_by_instance(obj)
        comments=CommentCreateSerializer(comments_qs,many=True).data
        return comments
