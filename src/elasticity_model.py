import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


class ElasticityModel:

    def __init__(self):
        self.elasticities = {}
    
    def fit(self, df):
        df = df.copy()

        #removing invalid rows
        df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]

        #log transformation
        df['log_price'] = np.log(df['Price'])
        df['log_quantity'] = np.log(df['Quantity'])

        # calculating the elasticity per StockCode
        for product, group in df.groupby('StockCode'):

            if len(group) < 10:
                continue

            X = group[['log_price']]
            y = group['log_quantity']

            model = LinearRegression()
            model.fit(X, y)

            elasticity = model.coef_[0]

            self.elasticities[product] = elasticity
        
    def get_elasticity(self, product_id):
        return self.elasticities.get(product_id, -1.0)
        