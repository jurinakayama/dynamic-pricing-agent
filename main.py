print('Activating Dynamic Pricing Agent ...\n')

print('Loading and cleaning data...')
from src.data_loader import df, pd

from src.elasticity_model import ElasticityModel
from src.pricing_engine import PricingEngine

def run_agent():
    print('\nTraining Elasticity Model (may take a few seconds)...')
    model = ElasticityModel()
    model.fit(df)

    print('\nInitializing Pricing Engine...')
    engine = PricingEngine(elasticity_model=model, strategy='profit')

    print('\nCalculating new optimal prices for the entire catalog...')
    product_prices = df.groupby('StockCode')['Price'].mean().reset_index()
    results = []
    total_products = len(product_prices)

    for index, row in product_prices.iterrows():
        product_id = row['StockCode']
        current_price = row['Price']

        elasticity = model.get_elasticity(product_id)

        new_price = engine.recommend_price(product_id=product_id, current_price=current_price)

        results.append({
            'StockCode': product_id,
            'CurrentPrice': round(current_price, 2),
            'Elasticity': round(elasticity, 4),
            'RecommendedPrice': new_price
        })

        if (index + 1) % 500 == 0:
            print(f'Processed {index + 1} / {total_products} products...')


    results_df = pd.DataFrame(results)

    output_file = 'data/updated_prices.csv'
    results_df.to_csv(output_file, index=False)

    print(f'Generated new optimal prices for {len(results_df)} products.')
    print(f'File saved to: {output_file}')

    print('\nPreview of the new catalog:')
    print(results_df.head(10))

if __name__ == '__main__':
    run_agent()
