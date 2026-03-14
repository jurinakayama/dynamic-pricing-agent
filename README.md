# Dynamic Pricing Agent 

## Overview
This dynamic pricing agent builds a machine learning system that analyzes the past product prices and estimates the elasticity using the retail transaction data and recommends the user optimal prices to maximize revenue while maintaining the demand. The system is subject to react and analyze how sensitive customers are to price changes and generates pricing recommendations by creating demand models based on regression. 

## Business Problem Statement
There is a shared common struggle within retailers to determine the optimal price point for products. 
- **Pricing too high** = the demand reduces
- **Pricing too low** = the revenue is sacrificed 
This pricing agent addresses this problem by dynamically adjusting and calculating the price elasticity of demand for each product and using it to produce different cases of revenue under different pricings. 

## Dataset
**Online Retail Dataset (UCI Machine Learning Repository)**
Consisted of following records:
* Invoice number
* Product ID (StockCode)
* Quantity purchased
* Price per item
* Customer ID
* Transaction timestamp
After preprocessing, data was:
* around 500,000 transactions
* around 4,000 products

## Methods Used
1. Data Cleaning (Cleans the raw transactional data given)
* Removed negative quantities, missing customer IDs for more relavant analysis
* Filtered invalid prices 

2. Feature Engineering
* used following log transformation for demand modeling
    $$\log(Q) = \beta_0 + \beta_1 \log(P)$$
where $\beta_1$ is price elasticity

3. Model
Linear regression model to estimate elasticity for each product

Libraries used
* pandas
* numpy
* scikit-learn

**Output Preview**
| StockCode | Current Price | Elasticity | Recommended Price |
| :--- | :--- | :--- | :--- |
| 10002 | $0.99 | -3.3586 | 0.790000 |
| 10002R | $5.13 | -1.0000 | 5.133333 |
| 10080 | $0.51 | -2.4923 | 0.420000 |
| 10109 | $0.42 | -1.0000 | 0.420000 |
| 10120 | $0.24 | -2.3059 | 0.210000 |

**Demand vs Price Model**
![Demand Curve for Product 85123A](demand_curve.png)

4. Pricing Engine
Recommends mathematically optimal price by application of economic formulas (e.g., Lerner Index) and business guardrails (e.g., +- 20% price)

Interpretation shows that
* Price Elastic (Elasticity < –1): Demand is sensitive to price
* Price Inelastic (Elasticity > -1): Demand is less sensitive to price



**KEY INSIGHTS**
* ~60% of products were elastic
* Reducing the price would increase revenue for highly elastic products


**INSTALLATION**
Clone the repository:
git clone https://github.com/yourusername/dynamic-pricing-agent.git cd dynamic-pricing-agent

Install:
pip install -r requirements.txt

Run pipeline:
python main.py

**Project Structure**
```text
dynamic-pricing-agent
│
├─ data 
│   ├─ online_retail_II.xlsx
│   ├─ online_retail_2009_2010.csv
│   └─ online_retail_2010_2011.csv
│
├─ app
│   └─ dashboard.py
│
├─ models 
├─ notebooks
│
├─ src  
│   ├─ data_loader.py
│   ├─ elasticity_model.py
│   └─ pricing_engine.py
│
├─ main.py
├─ README.md
└─ requirements.txt 
```

**Author**
*Juri Nakayama*
