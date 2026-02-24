import pandas as pd

file_path = 'data/online_retail_II.xlsx'
df1 = pd.read_excel(file_path, sheet_name='Year 2009-2010')
df2 = pd.read_excel(file_path, sheet_name='Year 2010-2011')
df1.to_csv('data/online_retail_2009_2010.csv', index=False)
df2.to_csv('data/online_retail_2010_2011.csv', index=False)


df1 = pd.read_csv('data/online_retail_2009_2010.csv')
df2 = pd.read_csv('data/online_retail_2010_2011.csv')

df = pd.concat([df1, df2])

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
df['Hour'] = df['InvoiceDate'].dt.hour

df['TotalSales'] = df['Quantity'] * df['Price']

# removing cancellations and returns for total revenue calculation
df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]

print(df.columns)
print(df.head())
