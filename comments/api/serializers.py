from rest_framework.serializers import( ModelSerializer,HyperlinkedIdentityField,SerializerMethodField)

from comments.models import Comments

def create_comment_serializer(model_type='Post',object_id=None,parent_id=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model=Comments
            fields=[
                "id",
                "object_id",
                "content",

            ]
        def __init__(self,*args,**kwargs):
            self.model_type=model_type
            self.object_id=object_id

    return CommentCreateSerializer


class CommentCreateSerializer(ModelSerializer):
    # reply_count=SerializerMethodField()
    class Meta:
            model=Comments
            fields=[
                "id",
                "content_type",
                "object_id",
                "content",
                # "reply_count", 
            ]

    # def get_reply_count(self,obj):
    #     if obj.is_parent():
    #         return obj.children().count()
    #     return None



class CommentChildSerializer(ModelSerializer):
    class Meta:
            model=Comments
            fields=[
                "id",
                "content",
                "timestamp",
                
               
            ]

class CommentDetailSerializer(ModelSerializer):
    # replies=SerializerMethodField()
    class Meta:
            model=Comments
            fields=[
                "id",
                "content_type",
                "object_id",
                "content",]
                # "replies", 

            read_only_fields=[
                "id",
                "content_type",
                "object_id",]

    # def get_replies(self,obj):
    #     if obj.is_parent:
    #         return CommentChildSerializer(obj.children,many=True).data
    #     return None

