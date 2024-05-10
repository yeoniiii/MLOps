from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd


class numeric_filtering(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.constant_col = [i for i in range(X.shape[1]) if X[:,i].std()==0]
        self.id_col = [i for i in range(X.shape[1]) if len(np.unique(np.diff(X[:,i])))==1]
        self.rm_cols = self.constant_col + self.id_col
        self.final_cols = [i for i in range(X.shape[1]) if i not in self.rm_cols]
        return self
    
    def transform(self, X):
        result = X[:,self.final_cols]
        return result
    
    
class categorical_filtering(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.constant_col = [i for i in range(X.shape[1]) if len(np.unique(X[:,i]))==1]
        self.id_col = [i for i in range(X.shape[1]) if len(np.unique(X[:,i]))==X.shape[0]]
        self.cardinality = [i for i in range(X.shape[1]) if len(np.unique(X[:,i])) > 50]
        self.rm_cols = self.constant_col + self.id_col + self.cardinality
        self.final_cols = [i for i in range(X.shape[1]) if i not in self.rm_cols]
        return self
    
    def transform(self, X):
        result = X[:,self.final_cols]
        return result