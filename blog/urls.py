from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    # path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    # path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new', views.PostCreateView.as_view(), name='post_new'),
    # path('post/new', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
    # path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('drafts/', views.PostDraftListView.as_view(), name='post_draft_list'),
    # path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.PostPublishView.as_view(), name='post_publish'),
    # path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/comment/', views.CommentCreateView.as_view(), name='add_comment_to_post'),
    # path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),
    # path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/remove/', views.CommentDeleteView.as_view(), name='comment_remove'),
    # path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('comment/<int:pk>/approve/', views.CommentApproveView.as_view(), name='comment_approve'),
    # path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
]