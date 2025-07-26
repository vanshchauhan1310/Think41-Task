import os
import csv
from pymongo import MongoClient
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from tqdm import tqdm  # for progress bars

# Load environment variables
load_dotenv()

# MongoDB Atlas connection
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'ecommerce')

def connect_to_mongodb():
    """Connect to MongoDB Atlas"""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        print("✅ Successfully connected to MongoDB Atlas")
        return db
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise

def chunk_insert(collection, data, chunk_size=1000):
    """Insert data in chunks to avoid overwhelming MongoDB"""
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        try:
            collection.insert_many(chunk, ordered=False)
        except Exception as e:
            print(f"⚠️ Partial insert error (some duplicates may exist): {str(e)[:200]}")

def load_distribution_centers(db, csv_file):
    """Load distribution centers data from CSV"""
    print("\n📦 Loading distribution centers...")
    collection = db['distribution_centers']
    collection.delete_many({})
    
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        centers = []
        
        for row in tqdm(reader, desc="Processing centers"):
            try:
                center = {
                    'id': int(row['id']),
                    'name': row['name'],
                    'location': {
                        'type': 'Point',
                        'coordinates': [
                            float(row['longitude']),
                            float(row['latitude'])
                        ]
                    },
                    'latitude': float(row['latitude']),
                    'longitude': float(row['longitude']),
                    'created_at': datetime.utcnow()
                }
                centers.append(center)
            except Exception as e:
                print(f"⚠️ Error processing center {row.get('id')}: {e}")
        
        if centers:
            chunk_insert(collection, centers)
            print(f"✅ Inserted {len(centers)} distribution centers")
            
            # Create indexes
            collection.create_index([('location', '2dsphere')])
            collection.create_index('id', unique=True)
            print("🔑 Created geospatial and ID indexes")

def load_products(db, csv_file):
    """Load products data from CSV"""
    print("\n👕 Loading products...")
    collection = db['products']
    collection.delete_many({})
    
    # Read CSV in chunks for large files
    chunksize = 10**5
    total_rows = 0
    
    for chunk in tqdm(pd.read_csv(csv_file, chunksize=chunksize), desc="Processing products"):
        products = []
        for _, row in chunk.iterrows():
            try:
                product = {
                    'id': int(row['id']),
                    'cost': float(row['cost']),
                    'category': row['category'],
                    'name': row['name'],
                    'brand': row['brand'],
                    'retail_price': float(row['retail_price']),
                    'department': row['department'],
                    'sku': row['sku'],
                    'distribution_center_id': int(row['distribution_center_id']),
                    'created_at': datetime.utcnow()
                }
                products.append(product)
            except Exception as e:
                print(f"⚠️ Error processing product {row.get('id')}: {e}")
        
        if products:
            chunk_insert(collection, products)
            total_rows += len(products)
    
    print(f"✅ Inserted {total_rows} products")
    
    # Create indexes
    collection.create_index('id', unique=True)
    collection.create_index('distribution_center_id')
    collection.create_index('category')
    print("🔑 Created product indexes")

def load_users(db, csv_file):
    """Load users data from CSV"""
    print("\n👤 Loading users...")
    collection = db['users']
    collection.delete_many({})
    
    # Assuming columns: id, name, email, etc.
    chunksize = 10**5
    total_rows = 0
    
    for chunk in tqdm(pd.read_csv(csv_file, chunksize=chunksize), desc="Processing users"):
        users = []
        for _, row in chunk.iterrows():
            try:
                user = {
                    'id': int(row['id']),
                    'name': row.get('name', ''),
                    'email': row.get('email', ''),
                    'created_at': datetime.utcnow()
                    # Add other fields as needed
                }
                users.append(user)
            except Exception as e:
                print(f"⚠️ Error processing user {row.get('id')}: {e}")
        
        if users:
            chunk_insert(collection, users)
            total_rows += len(users)
    
    print(f"✅ Inserted {total_rows} users")
    
    # Create indexes
    collection.create_index('id', unique=True)
    collection.create_index('email')
    print("🔑 Created user indexes")

def load_orders(db, csv_file):
    """Load orders data from CSV"""
    print("\n📝 Loading orders...")
    collection = db['orders']
    collection.delete_many({})
    
    # Assuming columns: id, user_id, status, etc.
    chunksize = 10**5
    total_rows = 0
    
    for chunk in tqdm(pd.read_csv(csv_file, chunksize=chunksize), desc="Processing orders"):
        orders = []
        for _, row in chunk.iterrows():
            try:
                order = {
                    'id': int(row['id']),
                    'user_id': int(row['user_id']),
                    'status': row.get('status', 'pending'),
                    'total_amount': float(row.get('total_amount', 0)),
                    'created_at': datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S') if 'created_at' in row else datetime.utcnow()
                    # Add other fields as needed
                }
                orders.append(order)
            except Exception as e:
                print(f"⚠️ Error processing order {row.get('id')}: {e}")
        
        if orders:
            chunk_insert(collection, orders)
            total_rows += len(orders)
    
    print(f"✅ Inserted {total_rows} orders")
    
    # Create indexes
    collection.create_index('id', unique=True)
    collection.create_index('user_id')
    collection.create_index('status')
    print("🔑 Created order indexes")

def load_order_items(db, csv_file):
    """Load order items data from CSV"""
    print("\n🛒 Loading order items...")
    collection = db['order_items']
    collection.delete_many({})
    
    # Assuming columns: id, order_id, product_id, quantity, etc.
    chunksize = 10**5
    total_rows = 0
    
    for chunk in tqdm(pd.read_csv(csv_file, chunksize=chunksize), desc="Processing order items"):
        items = []
        for _, row in chunk.iterrows():
            try:
                item = {
                    'id': int(row['id']),
                    'order_id': int(row['order_id']),
                    'product_id': int(row['product_id']),
                    'quantity': int(row.get('quantity', 1)),
                    'price': float(row.get('price', 0)),
                    'created_at': datetime.utcnow()
                }
                items.append(item)
            except Exception as e:
                print(f"⚠️ Error processing order item {row.get('id')}: {e}")
        
        if items:
            chunk_insert(collection, items)
            total_rows += len(items)
    
    print(f"✅ Inserted {total_rows} order items")
    
    # Create indexes
    collection.create_index('id', unique=True)
    collection.create_index('order_id')
    collection.create_index('product_id')
    print("🔑 Created order item indexes")

def load_inventory_items(db, csv_file):
    """Load inventory items data from CSV"""
    print("\n📊 Loading inventory items...")
    collection = db['inventory_items']
    collection.delete_many({})
    
    # Assuming columns: id, product_id, distribution_center_id, quantity, etc.
    chunksize = 10**5
    total_rows = 0
    
    for chunk in tqdm(pd.read_csv(csv_file, chunksize=chunksize), desc="Processing inventory"):
        items = []
        for _, row in chunk.iterrows():
            try:
                item = {
                    'id': int(row['id']),
                    'product_id': int(row['product_id']),
                    'distribution_center_id': int(row['distribution_center_id']),
                    'quantity': int(row.get('quantity', 0)),
                    'status': row.get('status', 'available'),
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
                items.append(item)
            except Exception as e:
                print(f"⚠️ Error processing inventory item {row.get('id')}: {e}")
        
        if items:
            chunk_insert(collection, items)
            total_rows += len(items)
    
    print(f"✅ Inserted {total_rows} inventory items")
    
    # Create indexe
    collection.create_index('id', unique=True)
    collection.create_index('product_id')
    collection.create_index('distribution_center_id')
    print("🔑 Created inventory indexes")

def main():
    print("🚀 Starting MongoDB Data Ingestion")
    
    # Connect to MongoDB
    db = connect_to_mongodb()
    
    # Load all data files
    try:
        # Adjust file paths as needed
        data_dir = './data'
        
        # Load each file if it exists
        if os.path.exists(f'{data_dir}/distribution_centers.csv'):
            load_distribution_centers(db, f'{data_dir}/distribution_centers.csv')
        
        if os.path.exists(f'{data_dir}/products.csv'):
            load_products(db, f'{data_dir}/products.csv')
        
        if os.path.exists(f'{data_dir}/users.csv'):
            load_users(db, f'{data_dir}/users.csv')
        
        if os.path.exists(f'{data_dir}/orders.csv'):
            load_orders(db, f'{data_dir}/orders.csv')
        
        if os.path.exists(f'{data_dir}/order_items.csv'):
            load_order_items(db, f'{data_dir}/order_items.csv')
        
        if os.path.exists(f'{data_dir}/inventory_items.csv'):
            load_inventory_items(db, f'{data_dir}/inventory_items.csv')
        
        print("\n🎉 All data loaded successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during data loading: {e}")
    finally:
        print("\n🏁 Data ingestion process completed")

if __name__ == '__main__':
    main()