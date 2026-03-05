print('Starting Dynamic Pricing Agent ...\n')

print('Loading and cleaning data...')
from src.data_loader import df

from src.elasticity_model import ElasticityModel
from src.pricing_engine import PricingEngine

def run_agent():
    print('\nTraining Elasticity Model (takes a few seconds)...')
    model = ElasticityModel()
    model.fit(df)

    print('\nInitializing Pricing Engine...')
    engine = PricingEngine(elasticity_model=model, strategy='profit')

    # Test on specific product
    test_product = '85123A'

    current_avg_price = df[df['StockCode'] == test_product]['Price'].mean()

    print(f'\n==============================')
    print(f'Pricing Recommendation')
    print(f'==============================')
    print(f'Product ID:   {test_product}')
    print(f'Current Price:   ${current_avg_price:.2f}')

    elasticity = model.get_elasticity(test_product)
    print(f'Elasticity:   {elasticity:.4f}')

    new_price = engine.recommend_price(product_id = test_product, current_price=current_avg_price)
    print(f'Optimal Price: ${new_price:.2f}')
    print(f'==============================\n')

if __name__ == '__main__':
    run_agent()
    