from django.conf.urls import url, include
from rest_framework import routers
from bukhach.views import page_views, authorization_views, dashboard_views, social_views, view_sets
from django.urls import path, re_path

router = routers.DefaultRouter()
router.register(r'users', view_sets.UserViewSet)
router.register(r'groups', view_sets.GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'', page_views.index_view),
    path(r'match', page_views.match_view),
    path(r'gay', page_views.gay_view),
    path(r'gtfo', page_views.fuck_yourself_view),
    path(r'appeals', page_views.appeals_view),

    # authentication
    path(r'register', authorization_views.register_view),
    path(r'register_user', authorization_views.register_user),
    path(r'login', authorization_views.login_view),
    path(r'login_user', authorization_views.login_user),
    path(r'logout', authorization_views.logout_user),

    # dashboard
    path(r'dashboard', dashboard_views.dashboard_view),
    path(r'add-interval', dashboard_views.accept_interval),
    path(r'people_search', dashboard_views.people_search),
    path(r'edit_profile', dashboard_views.edit_profile),
    path(r'edit_avatar', dashboard_views.edit_avatar),
    path(r'edit_password', dashboard_views.edit_password),

    # social
    re_path(r'^profile/(?P<profileId>\d+)/$', social_views.profile_view),
    path(r'add_friend', social_views.add_friend),
    path(r'delete_friend', social_views.delete_friend)
]
