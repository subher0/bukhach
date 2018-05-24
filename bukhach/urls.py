from django.conf.urls import url, include
from rest_framework import routers
from bukhach.views import page_views, authorization_views, dashboard_views, social_views
from bukhach.viewsets import profile_viewsets, gathering_viewsets, service_viewsets, intervals_and_match_viewsets
from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from bukhach.viewsets.intervals_and_match_viewsets import IntervalView, get_matches
from bukhach.viewsets.profile_viewsets import ProfileViewSet, ProfileSearchView
from bukhach.viewsets.service_viewsets import AppealsView

router = routers.SimpleRouter()

router.register(r'profiles', ProfileViewSet, base_name='profile')

urlpatterns = [
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
    re_path(r'profile/(?P<profileId>\d+)/$', social_views.profile_view),
    path(r'add_friend', social_views.add_friend),
    path(r'delete_friend', social_views.delete_friend),

    #rest_framework
    url(r'^api/v1/token-auth/', obtain_jwt_token),
    url(r'^api/v1/token-refresh/', refresh_jwt_token),
    url(r'^api/v1/token-verify/', verify_jwt_token),

    path(r'api/v1/profile_search', profile_viewsets.ProfileSearchView.as_view({'get': 'get'})),
    path(r'api/v1/intervals', intervals_and_match_viewsets.IntervalView.as_view()),
    re_path(r'api/v1/match/(?P<gathering_id>\d+)', get_matches),
    path(r'api/v1/appeal', service_viewsets.AppealsView.as_view()),

    url(r'^api/v1/', include(router.urls))
]