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
        print(f'Calculated elasticity for {len(self.elasticities)} products.')
        
    def get_elasticity(self, product_id):
        return self.elasticities.get(product_id, -1.0)
    
    def plot_demand_curve(self, product_id, df):
        import matplotlib.pyplot as plt

        product_df = df[df['StockCode'] == product_id].copy()

        if product_df.empty:
            print(f'ERROR; No data found for product #{product_id}')
            return
        
        if 'YearWeek' not in product_df.columns:
            product_df['InvoiceDate'] = pd.to_datetime(product_df['InvoiceDate'])
            product_df['YearWeek'] = product_df['InvoiceDate'].dt.strftime('%Y-%U')

        week_data = product_df.groupby('YearWeek').agg({'Price':'mean', 'Quantity':'sum'}).reset_index()

        plt.figure(figsize=(10,6))

        plt.scatter(week_data['Price'], week_data['Quantity'], color = 'blue', alpha=0.5, label='Actualy Weekly Sales')

        elasticity = self.get_elasticity(product_id)
        if elasticity != -1.0:
            x = np.linspace(week_data['Price'].min(), week_data['Price'].max(), 200)
            b = np.mean(np.log(week_data['Quantity'])) - elasticity * np.mean(np.log(week_data['Price']))
            y = np.exp(b) * (x ** elasticity)

            plt.plot(x,y, color='red', linewidth=1.5, label=f'Demand Curve (Elasticity: {elasticity:.3f})')
        
        plt.title(f'Demand vs. Price for Product: {product_id}')
        plt.xlabel('Average Weekly Price ($)')
        plt.ylabel('Total Weekly Quantity Sold')
        plt.legend()
        plt.grid(True, linestyle = '--', alpha = 0.8)
        plt.savefig('demand_curve.png', dpi=300, bbox_inches = 'tight')
        plt.show()
