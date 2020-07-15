from rest_framework.generics import (
        RetrieveUpdateAPIView,
        CreateAPIView,
        ListAPIView,
        RetrieveAPIView,
        DestroyAPIView,
        UpdateAPIView)
from comments.api.serializers import CommentCreateSerializer,CommentDetailSerializer
from django.db.models import Q
from rest_framework.filters import (SearchFilter,OrderingFilter)
from blog.api.pagination import PostLimitOffsetPagination,PostPageNumberPagination
from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

)
from blog.api.permissions import IsOwnerOrReadOnly
from rest_framework.mixins import DestroyModelMixin,UpdateModelMixin
from comments.models import Comments

class CommentCreateAPIView(CreateAPIView):
    queryset=Comments.objects.all()
    serializer_class=CommentCreateSerializer
    permission_classes=[IsAuthenticated]


    def perform_create(self, serializer):
         serializer.save(user=self.request.user)

class CommentListAPIView(ListAPIView):
    serializer_class=CommentCreateSerializer
    filter_backends=[SearchFilter,OrderingFilter]
    search_fields=['content','user__first_name']
    pagination_class=PostPageNumberPagination

    def get_queryset(self,*args,**kwargs):
            queryset=Comments.objects.all()
            query=self.request.GET.get("q")
            if query:
                queryset=queryset.filter(
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query)|
                    Q(user__last_name__icontains=query)
                    ).distinct()

            return queryset

# class PostDeleteAPIView(DestroyAPIView):
#     queryset=Post.objects.all()
#     serializer_class=PostDetailSerializer


class CommentDetailAPIView( DestroyModelMixin,UpdateModelMixin,RetrieveAPIView):
    queryset=Comments.objects.all()
    serializer_class=CommentDetailSerializer

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

# class PostUpdateAPIView(RetrieveUpdateAPIView):
#     queryset=Post.objects.all()
#     serializer_class=PostCreateUpdateSerializer
#     permission_classes=[IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

#     def perform_update(self, serializer):
#          serializer.save(user=self.request.user)
