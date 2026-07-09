from django.urls import path
from .views import CoverLetterView, MatchJobsView

urlpatterns = [
    path('cover-letter/', CoverLetterView.as_view(), name='cover_letter'),
    path('match-jobs/', MatchJobsView.as_view(), name='match_jobs'),
]
