from celery.worker.control import revoke
from django.contrib import admin
# Register your models here.
from django.http import HttpResponseRedirect
from django.urls import path

from app_store_ranking_v2.celery import app as celery_app
from app_store_ranking_v2.task_names import SCRAPE_AND_PROCESS_APP_RANKS
from apps.app_rank.models import ShopifyApp, Keyword, AppData, Session, AppRank, ScrapedHTML, RankDelta
from apps.app_rank.models.error_log import ErrorLog


@admin.register(ShopifyApp)
class ShopifyAppAdmin(admin.ModelAdmin):
    list_display = ('app_handle', 'name', 'developed_by', 'created_at')


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'keyword')


@admin.register(AppData)
class AppDataAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'shopify_app', 'reviews_rating', 'reviews_count', 'signifiers', 'categories', 'created_at')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    change_list_template = 'session_admin.html'
    list_display = ('id', 'session_uuid', 'status', 'details', 'modified_at', 'created_at')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('run_task/<str:keyword>', self.trigger_task),
            path('cancel_task/', self.cancel_task)
        ]
        return my_urls + urls

    def trigger_task(self, request, keyword='global'):
        print('keyword=', keyword)
        celery_app.send_task(name=SCRAPE_AND_PROCESS_APP_RANKS, args=(keyword,))

        self.message_user(request, 'Task Triggered')
        return HttpResponseRedirect("../")

    # This method does not work
    def cancel_task(self, request):
        # task = celery_app.Task.request
        task = celery_app.Task.request
        # revoke(task_id='abc', terminate=True, state=states.REVOKED)
        # self.message_user(request, 'Task Canceled')
        # task = celery_app.current_task
        print('task = ', task)
        # task_id = current_task.request.id
        if task:
            task_id = task.id
            print('task_id = ', task_id)
            revoke(task_id, terminate=True)
            self.message_user(request, 'Task Canceled')
        else:
            self.message_user(request, 'Task = None')
        return HttpResponseRedirect("../")


@admin.register(AppRank)
class AppRankAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopify_app', 'keyword', 'rank', 'session', 'created_at')


@admin.register(ScrapedHTML)
class ScrapedHTMLAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'page_no', 'app_handle', 'status', 'created_at')


@admin.register(RankDelta)
class RankDeltaAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopify_app', 'prev_rank', 'new_rank', 'session_id', 'rank_delta', 'created_at')


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'error_message', 'session_id', 'created_at')
    ordering = ('-created_at',)
