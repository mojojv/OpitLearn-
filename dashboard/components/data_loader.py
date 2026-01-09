"""
Data loading utilities for OpitLearn Dashboard
Handles loading and caching of parquet data
"""
import pandas as pd
from pathlib import Path
from functools import lru_cache

# Path to curated data
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "curated"
MASTER_TABLE = DATA_DIR / "master_table.parquet"

@lru_cache(maxsize=1)
def load_master_data():
    """Load the master table with caching"""
    if not MASTER_TABLE.exists():
        # Return empty dataframe if file doesn't exist
        return pd.DataFrame()
    
    df = pd.read_parquet(MASTER_TABLE)
    return df

def get_filtered_data(programa=None, estrato=None):
    """Get filtered data based on criteria"""
    df = load_master_data()
    
    if df.empty:
        return df
    
    if programa and programa != "Todos":
        df = df[df['programa'] == programa]
    
    if estrato and estrato != "Todos":
        df = df[df['estrato'] == int(estrato)]
    
    return df

def get_unique_programs():
    """Get list of unique programs"""
    df = load_master_data()
    if df.empty or 'programa' not in df.columns:
        return []
    return sorted(df['programa'].dropna().unique().tolist())

def get_unique_estratos():
    """Get list of unique estratos"""
    df = load_master_data()
    if df.empty or 'estrato' not in df.columns:
        return []
    return sorted(df['estrato'].dropna().unique().tolist())

def refresh_data():
    """Clear cache and reload data"""
    load_master_data.cache_clear()
    return load_master_data()
