from django.urls import path
from . import views

urlpatterns = [
    path('predict/<dataframe>',views.predict, name='predict'),
    ]
