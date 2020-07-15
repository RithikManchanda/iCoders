from django.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.



class CommentManager(models.Manager):
    def filter_by_instance(self,instance):
        content_type=ContentType.objects.get_for_model(instance.__class__)
        object_id=instance.id
        qs=super(CommentManager,self).filter(content_type= content_type,object_id=object_id)
        #Comments.objects
        return qs

class Comments(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    #post=models.ForeignKey(Post,on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    parent=models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    objects=CommentManager()

    def __str__(self):
        return self.user.username

    


    def children(self):
        return Comments.objects.filter(parent=self)

    @property
    def is_parent(self):                           #this property checks wether a given comment is a parent or not .if the parent of the comment exists the it is not a parent then it is a reply.
        if self.parent is not None:
            return False

        return True
          
    class Meta:
        #verbose_name = "comment" 
        ordering=["-timestamp"]  #showing the newest comment first