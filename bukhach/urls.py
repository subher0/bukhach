from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from bukhach.viewsets.intervals_and_match_viewsets import IntervalViewSet, get_matches
from bukhach.viewsets.profile_viewsets import ProfileViewSet, confirm
from bukhach.viewsets.service_viewsets import AppealsView
from bukhach.viewsets.gathering_viewsets import GatheringViewSet, GatheringApplicationViewSet
from bukhach.viewsets.friends_viewsets import FriendsViewSet

router = SimpleRouter()
router.register(r'profiles', ProfileViewSet, base_name='profiles')
router.register(r'friends', FriendsViewSet, base_name='friends')
router.register(r'gatherings', GatheringViewSet, base_name='gathering')

gathering_router = NestedSimpleRouter(router, r'gatherings', lookup='gathering')
gathering_router.register(r'applications', GatheringApplicationViewSet, base_name='application')
gathering_router.register(r'intervals', IntervalViewSet, base_name='interval')


urlpatterns = [
    # path(r'', page_views.index_view),
    # path(r'match', page_views.match_view),
    # path(r'gay', page_views.gay_view),
    # path(r'gtfo', page_views.fuck_yourself_view),
    # path(r'appeals', page_views.appeals_view),
    #
    # # authentication
    # path(r'register', authorization_views.register_view),
    # path(r'register_user', authorization_views.register_user),
    # path(r'login', authorization_views.login_view),
    # path(r'login_user', authorization_views.login_user),
    # path(r'logout', authorization_views.logout_user),
    #
    # # dashboard
    # path(r'dashboard', dashboard_views.dashboard_view),
    # path(r'add-interval', dashboard_views.accept_interval),
    # path(r'people_search', dashboard_views.people_search),
    # path(r'edit_profile', dashboard_views.edit_profile),
    # path(r'edit_avatar', dashboard_views.edit_avatar),
    # path(r'edit_password', dashboard_views.edit_password),
    #
    # # social
    # re_path(r'profile/(?P<profileId>\d+)/$', social_views.profile_view),
    # #re_path(r'gathering/(?P<gathering_id>\d+)/$', '')
    # path(r'add_friend', social_views.add_friend),
    # path(r'delete_friend', social_views.delete_friend),

    #rest_framework
    url(r'^api/v1/token-auth/', obtain_jwt_token),
    url(r'^api/v1/token-refresh/', refresh_jwt_token),
    url(r'^api/v1/token-verify/', verify_jwt_token),

#    path(r'api/v1/intervals', IntervalViewSet.as_view()),
    re_path(r'api/v1/match/(?P<gathering_id>\d+)', get_matches),
    path(r'api/v1/appeal', AppealsView.as_view()),
    path(r'api/v1/confirm-profile', confirm),

    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(gathering_router.urls))
]