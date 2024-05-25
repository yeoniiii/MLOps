import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.inspection import permutation_importance
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

class numeric_filtering(BaseEstimator, TransformerMixin):
    def __init__(self, check_const_col=True, check_id_col=True):
        self.check_const_col = check_const_col
        self.check_id_col = check_id_col

    def fit(self, X, y=None):
        if self.check_const_col:
            self.constant_col = [i for i in range(X.shape[1]) if X[:,i].std()==0]
        else:
            self.constant_col = []

        if self.check_id_col:
            self.id_col = [i for i in range(X.shape[1]) if len(np.unique(np.diff(X[:,i])))==1]
        else:
            self.id_col = []
            
        self.rm_cols = self.constant_col + self.id_col
        self.final_cols = [i for i in range(X.shape[1]) if i not in self.rm_cols]
        return self
  

    def transform(self, X):
        result = X[:,self.final_cols]
        return result
    
    
class categorical_filtering(BaseEstimator, TransformerMixin):

    def __init__(self, check_const_col=True, check_id_col=True, check_cardinality=True):
        self.check_const_col = check_const_col
        self.check_id_col = check_id_col
        self.check_cardinality = check_cardinality
  
    def fit(self, X, y=None):
        if self.check_const_col:
            self.constant_col = [i for i in range(X.shape[1]) if len(np.unique(X[:,i]))==1]
        else:
            self.constant_col = []

        if self.check_id_col:
            self.id_col = [i for i in range(X.shape[1]) if len(np.unique(X[:,i]))==X.shape[0]]
        else:
            self.id_col = []

        if self.check_cardinality:
            self.cardinality = [i for i in range(X.shape[1]) if len(np.unique(X[:,i])) > 50]
        else:
            self.cardinality = []

        self.rm_cols = self.constant_col + self.id_col + self.cardinality
        self.final_cols = [i for i in range(X.shape[1]) if i not in self.rm_cols]
        return self
  
    def transform(self, X):
        result = X[:,self.final_cols]
        return result





class pipeline_model:
    def __init__(self, params=None):        
        if params is None:
            self.is_cv = False
            self.n_perm = 5
        else:
            self.is_cv = True
            self.n_cv = params['n_cv']
            self.n_perm = params['n_perm']
            self.param_grid = {k: params[k] for k in params.keys() if k not in ['n_cv','n_perm']}
        
        pipe1 = Pipeline([
            ('step1',   SimpleImputer(strategy="mean") ),
            ('step2',   numeric_filtering()  ),
            ('step3',   StandardScaler()  ),
        ]) 
        
        pipe2 = Pipeline([
            ('step1',   SimpleImputer(strategy="most_frequent") ),
            ('step2',   categorical_filtering()  ),
            ('step3',   OneHotEncoder()  ),
        ])
        
        transform = ColumnTransformer([
            ('num',  pipe1,  make_column_selector(dtype_include=np.number)),
            ('cat',  pipe2,  make_column_selector(dtype_exclude=np.number)),
        ])
        
        pipe = Pipeline([
            ('transform',  transform ),
            ('model',      RandomForestClassifier() ),
        ])
        
        if self.is_cv:
            self.gs = GridSearchCV(pipe,
                                   param_grid=self.param_grid,
                                   scoring='accuracy',
                                   cv = self.n_cv,)
        else:
            self.gs = pipe                                        
        
    def fit(self, X, y):
        self.columns = X.columns.tolist()
        self.gs.fit(X, y)
        self.imp = permutation_importance(estimator = self.gs,
                                          X = X, y = y, 
                                          scoring="accuracy", 
                                          n_repeats=self.n_perm )
        return self
    
    def predict(self, X):
        return self.gs.predict(X)
        
    def feature_importances(self):
        result = pd.DataFrame(self.imp['importances_mean'], 
                              index=self.columns, columns=['features']).sort_values('features')
        return result
    
    def cv_result(self):
        result = pd.DataFrame(self.gs.cv_results_).sort_values('rank_test_score')
        return result






class ensemble_pipeline:
    def __init__(self):        
        pipe1 = Pipeline([
            ('step1',   SimpleImputer(strategy="mean") ),
            ('step2',   numeric_filtering()  ),
            ('step3',   StandardScaler()  ),
        ]) 
        
        pipe2 = Pipeline([
            ('step1',   SimpleImputer(strategy="most_frequent") ),
            ('step2',   categorical_filtering()  ),
            ('step3',   OneHotEncoder()  ),
        ])
        
        transform = ColumnTransformer([
            ('num',  pipe1,  make_column_selector(dtype_include=np.number)),
            ('cat',  pipe2,  make_column_selector(dtype_exclude=np.number)),
        ])

        self.models = {'RF':RandomForestClassifier(),
                       'LGBM':LGBMClassifier(),
                       'XGBM':XGBClassifier()
        }        
        
        ensemble_models = []
        for model in self.models.keys():
            pipe0 = Pipeline([
                ('transform', transform ),
                ('model', self.models[model] )
            ])
            ensemble_models.append( (model, pipe0) )
        
        self.ensemble_pipe = VotingClassifier(ensemble_models, voting="soft", verbose=0)        
        
    def fit(self, X, y):
        self.columns = X.columns.tolist()
        self.ensemble_pipe.fit(X, y)
        self.imp = permutation_importance(estimator = self.ensemble_pipe,
                                          X = X, y = y, 
                                          scoring="accuracy", 
                                          n_repeats=5 )
        return self
    
    def predict(self, X):
        pred = pd.DataFrame(self.ensemble_pipe.predict_proba(X)[:,0], columns=['ensemble'])
        for model in self.models.keys():
            pred[model] = self.ensemble_pipe.named_estimators_[model].predict_proba(X)[:,0]
        return pred



        return self.ensemble_pipe.predict(X)
        
    def feature_importances(self):
        result = pd.DataFrame(self.imp['importances_mean'], 
                              index=self.columns, 
                              columns=['features']).sort_values('features')
        return result






















