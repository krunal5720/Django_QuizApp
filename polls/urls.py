from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path('list/', views.polls_list, name='list'),
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('<int:poll_id>/vote/', views.poll_vote, name='vote'),
    path('poll_result/', views.poll_result, name='poll_result'),
    path('end_poll/', views.end_poll, name='end_poll'),
    path('quiz_history/', views.quiz_history, name='quiz_history'),
]
