from sklearn.base import BaseEstimator, TransformerMixin


class DataFrameToArrayTransformer(BaseEstimator, TransformerMixin):
    def fit(self, data_x, data_y=None):
        return self

    def transform(self, data_x, data_y=None):
        return data_x.toarray()
