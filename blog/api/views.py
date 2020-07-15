from rest_framework.generics import (
        RetrieveUpdateAPIView,
        CreateAPIView,
        ListAPIView,
        RetrieveAPIView,
        DestroyAPIView,
        UpdateAPIView)
from blog.api.serializers import PostListSerializer,PostDetailSerializer,PostCreateUpdateSerializer
from django.db.models import Q
from rest_framework.filters import (SearchFilter,OrderingFilter)
from.pagination import PostLimitOffsetPagination,PostPageNumberPagination
from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

)
from .permissions import IsOwnerOrReadOnly
from blog.models import Post

class PostCreateAPIView(CreateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostCreateUpdateSerializer
    permission_classes=[IsAuthenticated]


    def perform_create(self, serializer):
         serializer.save(user=self.request.user)

class PostListAPIView(ListAPIView):
    serializer_class=PostListSerializer
    filter_backends=[SearchFilter,OrderingFilter]
    search_fields=['title','content','user__first_name']
    pagination_class=PostPageNumberPagination

    def get_queryset(self,*args,**kwargs):
            queryset=Post.objects.all()
            query=self.request.GET.get("q")
            if query:
                queryset=queryset.filter(
                    Q(title__icontains=query)|
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query)|
                    Q(user__last_name__icontains=query)
                    ).distinct()

            return queryset

class PostDeleteAPIView(DestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostDetailSerializer

class PostDetailAPIView(RetrieveAPIView):
    queryset=Post.objects.all()
    serializer_class=PostDetailSerializer


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostCreateUpdateSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    def perform_update(self, serializer):
         serializer.save(user=self.request.user)



from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^$', schema_view)
]