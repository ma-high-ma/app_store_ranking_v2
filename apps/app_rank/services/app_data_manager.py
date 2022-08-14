class AppDataManager:
    def create_app_data(self, kwargs):
        return {
            'shopify_app_id': kwargs.get('app_handle'),
            'reviews_count': kwargs.get(review['review_count']),
            'reviews_rating': review['review_rating'],
            'signifiers': signifiers,
            'categories': categories,
            'pricing': pricing,
            'extras': self.get_extras()
        }
