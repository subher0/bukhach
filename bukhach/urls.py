from django.urls import path

from bukhach.views import main_view

urlpatterns = [
    path(r'', main_view.index_view),
    path(r'about', main_view.about_us_view),
    path(r'match', main_view.match_view),
    path(r'contacts', main_view.contacts_view),
    path(r'register', main_view.register_view),
]