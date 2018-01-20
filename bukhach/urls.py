from django.urls import path

from bukhach.views import main_views, authorization_views

urlpatterns = [
    path(r'', main_views.index_view),
    path(r'about', main_views.about_us_view),
    path(r'match', main_views.match_view),
    path(r'contacts', main_views.contacts_view),
    path(r'register', authorization_views.register_view),
    path(r'login', authorization_views.login_view),
]