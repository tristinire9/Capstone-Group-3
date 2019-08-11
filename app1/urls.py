from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # ex: /app1/1
    path('1', views.page1, name='page1'),
    path('2', views.page2, name='page2'),


    # ex: /app1/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /app1/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /app1/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
