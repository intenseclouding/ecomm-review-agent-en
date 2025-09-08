import sqlite3
import json
from datetime import datetime

def create_database():
    # Create database connection
    conn = sqlite3.connect('ecommerce_reviews.db')
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            seller_id TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT,
            image_url TEXT,
            features TEXT,  -- JSON array as text
            average_rating REAL DEFAULT 0.0,
            review_count INTEGER DEFAULT 0,
            rating_distribution TEXT  -- JSON object as text
        )
    ''')
    
    # Create reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id TEXT PRIMARY KEY,
            product_id TEXT NOT NULL,
            user_name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            verified_purchase BOOLEAN DEFAULT 1,
            auto_response TEXT,
            response_approved BOOLEAN DEFAULT 0,
            keywords TEXT,  -- JSON array as text
            sentiment TEXT,  -- JSON object as text
            analysis_completed BOOLEAN DEFAULT 0,
            analysis_timestamp TEXT,
            agent_log_id TEXT,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Create seller_responses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seller_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_id TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (review_id) REFERENCES reviews (id)
        )
    ''')
    
    # Create media_files table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media_files (
            id TEXT PRIMARY KEY,
            review_id TEXT NOT NULL,
            type TEXT NOT NULL,
            url TEXT NOT NULL,
            filename TEXT NOT NULL,
            size INTEGER NOT NULL,
            thumbnail_url TEXT,
            FOREIGN KEY (review_id) REFERENCES reviews (id)
        )
    ''')
    
    # Create agent_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_logs (
            id TEXT PRIMARY KEY,
            review_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            total_duration_ms INTEGER,
            status TEXT NOT NULL,
            steps TEXT,  -- JSON array as text
            metadata TEXT,  -- JSON object as text
            is_sample BOOLEAN DEFAULT 0,
            FOREIGN KEY (review_id) REFERENCES reviews (id)
        )
    ''')
    
    # Load and insert sample data
    with open('data/sample_products.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for product in data['products']:
        # Insert product
        cursor.execute('''
            INSERT OR REPLACE INTO products 
            (id, name, category, seller_id, price, description, image_url, features, 
             average_rating, review_count, rating_distribution)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product['id'],
            product['name'],
            product['category'],
            product['seller_id'],
            product['price'],
            product['description'],
            product['image_url'],
            json.dumps(product['features']),
            product['average_rating'],
            product['review_count'],
            json.dumps(product['rating_distribution'])
        ))
        
        # Insert reviews
        for review in product['reviews']:
            cursor.execute('''
                INSERT OR REPLACE INTO reviews 
                (id, product_id, user_name, rating, content, date, verified_purchase,
                 auto_response, response_approved, keywords, sentiment, 
                 analysis_completed, analysis_timestamp, agent_log_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                review['id'],
                product['id'],
                review['user_name'],
                review['rating'],
                review['content'],
                review['date'],
                review['verified_purchase'],
                review.get('auto_response'),
                review.get('response_approved', False),
                json.dumps(review.get('keywords')) if review.get('keywords') else None,
                json.dumps(review.get('sentiment')) if review.get('sentiment') else None,
                review.get('analysis_completed', False),
                review.get('analysis_timestamp'),
                review.get('agent_log_id')
            ))
            
            # Insert seller response if exists
            if review.get('seller_response'):
                cursor.execute('''
                    INSERT OR REPLACE INTO seller_responses (review_id, content, date)
                    VALUES (?, ?, ?)
                ''', (
                    review['id'],
                    review['seller_response']['content'],
                    review['seller_response']['date']
                ))
            
            # Insert media files if exist
            if review.get('media_files'):
                for media in review['media_files']:
                    cursor.execute('''
                        INSERT OR REPLACE INTO media_files 
                        (id, review_id, type, url, filename, size, thumbnail_url)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        media['id'],
                        review['id'],
                        media['type'],
                        media['url'],
                        media['filename'],
                        media['size'],
                        media.get('thumbnail_url')
                    ))
    
    conn.commit()
    conn.close()
    print("Database created successfully: ecommerce_reviews.db")

if __name__ == "__main__":
    create_database()