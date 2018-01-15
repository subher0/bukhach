from django.urls import path

from gobuhatwithme.site.views import main_view

urlpatterns = [
    path(r'', main_view.index_view),
]