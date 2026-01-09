import pandas as pd

# Load the curated data
df = pd.read_parquet('data/curated/master_table.parquet')

print('=== DATA QUALITY REPORT ===\n')
print(f'Total Records: {len(df)}')
print(f'Total Columns: {len(df.columns)}')
print(f'\nColumns: {list(df.columns)}')
print(f'\nMissing Values:\n{df.isnull().sum()}')
print(f'\nUnique Students: {df["estudiante_id"].nunique()}')
print(f'\nPrograms Distribution:')
print(df['programa'].value_counts())
print(f'\nSample Data (first 3 rows):')
print(df.head(3))
