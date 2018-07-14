from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from bukhach.views import page_views, authorization_views, dashboard_views, social_views
from bukhach.viewsets import profile_viewsets, group_viewsets, service_viewsets, intervals_and_match_viewsets
from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from bukhach.viewsets.friends_viewsets import FriendsViewSet
from bukhach.viewsets.profile_viewsets import ProfileViewSet

router = SimpleRouter()
router.register(r'profiles', ProfileViewSet, base_name='profiles')
router.register(r'friends', FriendsViewSet, base_name='friends')

urlpatterns = [

    # social
    re_path(r'profile/(?P<profileId>\d+)/$', social_views.profile_view),
    path(r'add_friend', social_views.add_friend),
    path(r'delete_friend', social_views.delete_friend),

    #rest_framework
    url(r'^api/v1/token-auth/', obtain_jwt_token),
    url(r'^api/v1/token-refresh/', refresh_jwt_token),
    url(r'^api/v1/token-verify/', verify_jwt_token),
    path(r'api/v1/profile-search/', profile_viewsets.ProfileSearchView.as_view()),
    path(r'api/v1/intervals', intervals_and_match_viewsets.IntervalView.as_view()),
    path(r'api/v1/match', intervals_and_match_viewsets.MatchView.as_view()),
    path(r'api/v1/appeal', service_viewsets.AppealsView.as_view()),
    path(r'api/v1/', include(router.urls))
]
