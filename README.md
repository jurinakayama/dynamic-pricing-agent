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
1. Data Cleaning
* Removed negative quantities 
* Removed missing customer IDs
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

Interpretation shows that
* Price Elastic (Elasticity < –1): Demand is sensitive to price
* Price Inelastic (Elasticity > -1): Demand is less sensitive to price



**KEY INSIGHTS**
* ~60% of products were elastic
* Reducing the price would increase revenue for highly elastic products



**Author**
*Juri Nakayama*
