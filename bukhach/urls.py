from django.urls import path, re_path

from bukhach.views import page_views, authorization_views, dashboard_views

urlpatterns = [
    path(r'', page_views.index_view),
    path(r'about', page_views.about_us_view),
    path(r'match', page_views.match_view),
    path(r'contacts', page_views.contacts_view),


    #authentication
    path(r'register', authorization_views.register_view),
    path(r'login', authorization_views.login_view),
    path(r'logout', authorization_views.logout_user),

    #dashboard
    path(r'dashboard', dashboard_views.dashboard_view),
    path(r'add-interval', dashboard_views.accept_interval),
    path(r'people_search', dashboard_views.people_search),
    re_path(r'^profile/(?P<profileId>\d+)/$', dashboard_views.profile_view),
]
