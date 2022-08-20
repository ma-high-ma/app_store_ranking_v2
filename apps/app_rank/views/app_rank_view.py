from datetime import timedelta

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.app_rank.services.basic_utils import BasicUtils, get_app_rank_data, get_app_data_diff


class AppRankingView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'index.html'

    def get(self, request):
        return Response()


class AppRankingResponseView(APIView):
    # renderer_classes = (TemplateHTMLRenderer,)
    # template_name = 'index.html'

    def get(self, request):
        print('HEYYYYYY')
        app_handle = request.GET.get('app_handle')
        start_date = request.GET.get('start_date', '2022-07-22')
        end_date = request.GET.get('end_date', '2022-07-31')
        print('REQUEST RESPONSE = ', request.GET)
        start_date = BasicUtils.convert_time_to_datetime(start_date)
        end_date = BasicUtils.convert_time_to_datetime(end_date)
        end_date = end_date + timedelta(days=1)
        result = get_app_rank_data(
            app_handle=app_handle,
            start_date=start_date,
            end_date=end_date
        )
        result = {
            "result": result,
            "diff": get_app_data_diff(
                app_handle=app_handle,
                start_date=start_date,
                end_date=end_date
            )
        }
        return Response(data=result)
