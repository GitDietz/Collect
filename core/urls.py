"""
for use with site administration efforts like updating lists
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from .views import admin, upload_csv


app_name = 'core'

urlpatterns = [
    path('admin', admin, name='admin'),
    path('^upload/csv/$', upload_csv, name='upload_csv'),
    # path('home_colors/', recipe.home_colors, name='home_colors'),
    # re_path('ingredient/(?P<pk>\d+)', recipe.ingredient_detail, name='ingredient_detail'),
    # path('ingredient_add_ajax/', recipe.ingredient_add_ajax, name='ingredient_add_ajax'),
]

# TODO get the direct to the admin base page working, then add links to the upload view