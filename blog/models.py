from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from comments.models import Comments
from django.contrib.contenttypes.models import ContentType

#MODEL MANAGERS
#Posts.objects.all()
#Posts.objects.create()
class PostManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(PostManager,self).filter(draft=False).filter(published__lte=timezone.now())

class Post(models.Model):
      user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
      title=models.CharField(max_length=100)
      slug=models.SlugField(max_length=150,default=' ')
      image=models.ImageField(null=True,blank=True,height_field="height_field",width_field="width_field")
      height_field=models.IntegerField(default=0)
      width_field=models.IntegerField(default=0)
      draft=models.BooleanField(default=False)
      published=models.DateField(auto_now=False,auto_now_add=False,default=timezone.now)
      content=models.TextField(max_length=200)
      updated=models.DateTimeField(auto_now=True,auto_now_add=False)
      timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)

      objects=PostManager()


      def __str__(self):
          return self.title


      def get_absolute_url(self):
          
          return "/blog/BlogPost/%s" %(self.id)

      def get_markdown(self):

          content=self.content
          markdown_text=markdown(content)
          return mark_safe( markdown_text)
      @property
      def comments(self):
          instance=self
          qs=Comments.objects.filter_by_instance(instance)
          return qs
      @property
      def get_content_type(self):
          instance=self
          content_type=ContentType.objects.get_for_model(instance.__class__)
          return content_type

      class Meta:
          verbose_name = "Post" 
          ordering=["-timestamp","-updated"]

    

#def create_slug(instance,new_slug=None):
   # slug=slugify(instance,title)
   # if new_slug is not None:
       #   slug=new_slug
   # qs=Contact.objects.filter(slug=slug).order_by("-id")
    #exists=qs.exists()
    #if exists:
    #   new_slug="%s-%s" %(slug, qs.first().id)
      # return create_slug(instance,new_slug=new_slug)
   # return slug




#def pre_save_post_receiver(sender,instance,*args,**kwargs):
   # if not instance.slug:

      #  instance.slug=create_slug(instance)


#pre_save.connect(pre_save_post_receiver,sender=Post)