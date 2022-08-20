from django.urls import path

from apps.app_rank.views.app_rank_view import AppRankingView, AppRankingResponseView

urlpatterns = [
    path('app-ranking/', AppRankingView.as_view(), name='html-home-page'),
    path('app-ranking-response/', AppRankingResponseView.as_view(), name='app-rank-graph-response'),
    # path('app-data-response/', AppDataDiffView.as_view(), name='app-data-diff-response'),
]
