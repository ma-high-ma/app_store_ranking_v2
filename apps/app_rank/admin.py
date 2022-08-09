from django.contrib import admin

# Register your models here.
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
        'id', 'shopify_app', 'reviews_rating', 'reviews_count', 'signifiers', 'filter_keywords', 'created_at')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_id', 'status', 'details', 'modified_at', 'created_at')


@admin.register(AppRank)
class AppRankAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopify_app', 'keyword', 'rank', 'session', 'created_at')


@admin.register(ScrapedHTML)
class ScrapedHTMLAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'page_no', 'app_handle', 'content', 'created_at')


@admin.register(RankDelta)
class RankDeltaAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopify_app', 'prev_rank', 'new_rank', 'session_id', 'rank_delta', 'created_at')


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'error_message', 'session', 'created_at')
    ordering = ('-created_at',)
