from sklearn.base import BaseEstimator, TransformerMixin
class DataFrameToArrayTransformer(BaseEstimator,TransformerMixin):    
    def __init__(self):
        None
    def fit(self, data_x,data_y=None):
        return self

    def transform(self, data_x,data_y=None):
        return data_x.toarray()
