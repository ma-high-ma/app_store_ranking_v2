import datetime
import hashlib
import json
from typing import Dict, Any

from apps.app_rank.models import AppRank, AppData


def get_app_rank_data(app_handle, start_date, end_date):
    print('hey am inside get_app_rank_data')

    result = []
    shopify_apps_rank = AppRank.objects.filter(
        shopify_app_id=app_handle,
        created_at__range=[start_date, end_date]
    ).values_list('rank', 'created_at')
    for i in shopify_apps_rank:
        x = {
            'app_handle': app_handle,
            # 'dev_by': dev_by,
            'rank': i[0],
            'created_at': i[1]
        }
        result.append(x)
    print('RESULT = ', result)

    print('Ranks = ', shopify_apps_rank)
    return result


def get_app_data_diff(app_handle, start_date, end_date):
    print('hey am inside get_app_data_diff')
    result = []
    app_data = AppData.objects.filter(
        shopify_app_id=app_handle,
        created_at__range=[start_date, end_date]
    ).distinct()
    for index, each_app_data in enumerate(app_data):
        print('app-data = ', each_app_data.__dict__)
        d = BasicUtils.convert_app_data_obj_into_dict(each_app_data)

        result.append(d)
    print(result)
    return result


class BasicUtils:
    @staticmethod
    def get_text_from_html_element(html_element):
        if html_element is None:
            return ''
        return html_element.text.replace('\\n', '').strip()

    @staticmethod
    def get_dict_hash(dictionary: Dict[str, Any]) -> str:
        """MD5 hash of a dictionary."""
        dhash = hashlib.md5()
        # We need to sort arguments so that {'a': 1, 'b': 2} is
        # the same as {'b': 2, 'a': 1}
        encoded = json.dumps(dictionary, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.hexdigest()

    @staticmethod
    def convert_time_to_datetime(time_data):
        t = datetime.datetime.strptime(time_data, "%Y-%m-%d")
        t = t.replace(tzinfo=datetime.timezone.utc)
        return t

    @staticmethod
    def convert_app_data_obj_into_dict(obj):
        return {
            'shopify_app_id': obj.shopify_app_id,
            'reviews_count': obj.reviews_count,
            'reviews_rating': obj.reviews_rating,
            'signifiers': obj.signifiers,
            'categories': obj.categories,
            'pricing': obj.pricing,
            'extras': obj.extras,
            'created_at': obj.created_at.strftime("%Y-%m-%d")
        }
