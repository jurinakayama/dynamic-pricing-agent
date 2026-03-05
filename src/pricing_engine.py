import numpy as np

class PricingEngine:
    
    def __init__(self, elasticity_model, strategy='profit'):
        self.elasticity_model = elasticity_model
        self.strategy = strategy

    def recommend_price(self, product_id, current_price, item_cost = None):
        elasticity = self.elasticity_model.get_elasticity(product_id)

        # if model return -1.0, don't have enough data to change the price safely 
        if elasticity == -1.0:
            return current_price
        
        if item_cost is None:
            item_cost = current_price * 0.50
        
        if self.strategy == 'profit':
            if elasticity < -1:
                optimal_price = item_cost * (elasticity / (elasticity + 1))
            else: 
                optimal_price = current_price * 1.20
        
        elif self.strategy == 'revenue':
            if elasticity < -1:
                optimal_price = current_price * 0.95
            else:
                optimal_price = current_price * 1.10
        else:
            optimal_price = current_price
        
       # –– Business Guardrails –– 

        # constrain price change (+- 20%)
        optimal_price = np.clip(
            optimal_price,
            current_price * 0.8,
            current_price * 1.2
        )

        if optimal_price < item_cost:
            optimal_price = item_cost * 1.05

        return round(optimal_price, 2)