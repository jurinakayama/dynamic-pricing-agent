import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


class ElasticityModel:

    def __init__(self):
        self.elasticities = {}
    
    def fit(self, df):
        df = df.copy()
        df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]

        if 'YearWeek' not in df.columns and 'InvoiceDate' in df.columns:
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
            df['YearWeek'] = df['InvoiceDate'].dt.strftime('%Y-%U')

        # time aggregation: group by product and week
        # need average price and total quantity sold per week 
        week_data = df.groupby(['StockCode', 'YearWeek']).agg({
            'Price': 'mean',
            'Quantity': 'sum'
        }).reset_index()

        #log transformation
        week_data['log_price'] = np.log(week_data['Price'])
        week_data['log_quantity'] = np.log(week_data['Quantity'])

        # calculating the elasticity per StockCode
        for product, group in week_data.groupby('StockCode'):
            if len(group) < 5:
                continue

            if group['log_price'].nunique() <= 1:
                continue

            X = group[['log_price']]
            y = group['log_quantity']

            model = LinearRegression()
            model.fit(X, y)

            elasticity = model.coef_[0]

            if elasticity > 0:
                elasticity = -0.5

            self.elasticities[product] = elasticity
        print(f'Model trained! Calculated elasticity for {len(self.elasticities)} products.')
        
    def get_elasticity(self, product_id):
        return self.elasticities.get(product_id, -1.0)

