from django.urls import path, re_path

from bukhach.views import page_views, authorization_views, dashboard_views, social_views

urlpatterns = [
    path(r'', page_views.index_view),
    path(r'match', page_views.match_view),
    path(r'gay', page_views.gay_view),


    #authentication
    path(r'register', authorization_views.register_view),
    path(r'register_user', authorization_views.register_user),
    path(r'login', authorization_views.login_view),
    path(r'login_user', authorization_views.login_user),
    path(r'logout', authorization_views.logout_user),

    #dashboard
    path(r'dashboard', dashboard_views.dashboard_view),
    path(r'add-interval', dashboard_views.accept_interval),
    path(r'people_search', dashboard_views.people_search),
    path(r'edit_profile', dashboard_views.edit_profile),

    #social
    re_path(r'^profile/(?P<profileId>\d+)/$', social_views.profile_view),
    path(r'add_friend', social_views.add_friend),
    path(r'delete_friend',social_views.delete_friend)
]
