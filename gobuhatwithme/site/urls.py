from django.urls import path

from gobuhatwithme.site.views import main_view

urlpatterns = [
    path(r'', main_view.index_view),
    path(r'about', main_view.about_us_view),
    path(r'match', main_view.match_view),
]