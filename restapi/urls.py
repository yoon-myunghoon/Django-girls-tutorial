from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('posts', views.PostViewSet)
router.register('comments', views.CommentViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]