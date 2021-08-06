import datetime
from haystack import indexes
from .models import Movie


class MoviePostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    director = indexes.CharField(model_attr='director')
    writers = indexes.CharField(model_attr='writers')
    stars = indexes.CharField(model_attr='stars')

    def get_model(self):
        return Movie

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # return self.get_model().objects.filter(updated__lte=datetime.datetime.now())
        return self.get_model().objects.all()