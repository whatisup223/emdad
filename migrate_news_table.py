#!/usr/bin/env python3
"""
Migration script to add new columns to the news table
Run this script to update your database schema
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add new columns to the news table"""
    
    # Database path
    db_path = 'instance/emdad_global.db'
    
    if not os.path.exists(db_path):
        print("Database file not found. Please make sure the database exists.")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Starting database migration...")
        
        # List of new columns to add
        new_columns = [
            # Enhanced Keywords
            ("focus_keyword_en", "VARCHAR(100)"),
            ("focus_keyword_ar", "VARCHAR(100)"),
            
            # Enhanced SEO
            ("seo_title_en", "VARCHAR(70)"),
            ("seo_title_ar", "VARCHAR(70)"),
            ("seo_description_en", "VARCHAR(160)"),
            ("seo_description_ar", "VARCHAR(160)"),
            
            # Open Graph
            ("og_title_en", "VARCHAR(95)"),
            ("og_title_ar", "VARCHAR(95)"),
            ("og_description_en", "VARCHAR(200)"),
            ("og_description_ar", "VARCHAR(200)"),
            ("og_image", "VARCHAR(255)"),
            
            # Twitter Card
            ("twitter_title_en", "VARCHAR(70)"),
            ("twitter_title_ar", "VARCHAR(70)"),
            ("twitter_description_en", "VARCHAR(200)"),
            ("twitter_description_ar", "VARCHAR(200)"),
            
            # Schema.org
            ("article_type", "VARCHAR(50) DEFAULT 'Article'"),
            
            # Content metadata
            ("estimated_reading_time", "INTEGER"),
            ("content_difficulty", "VARCHAR(20) DEFAULT 'intermediate'"),
        ]
        
        # Check which columns already exist
        cursor.execute("PRAGMA table_info(news)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        
        # Add new columns that don't exist
        added_columns = []
        for column_name, column_type in new_columns:
            if column_name not in existing_columns:
                try:
                    sql = f"ALTER TABLE news ADD COLUMN {column_name} {column_type}"
                    cursor.execute(sql)
                    added_columns.append(column_name)
                    print(f"✓ Added column: {column_name}")
                except sqlite3.Error as e:
                    print(f"✗ Error adding column {column_name}: {e}")
        
        # Update existing records with default values
        if added_columns:
            print("\nUpdating existing records with default values...")
            
            # Set default values for new columns
            update_queries = [
                "UPDATE news SET article_type = 'Article' WHERE article_type IS NULL",
                "UPDATE news SET content_difficulty = 'intermediate' WHERE content_difficulty IS NULL",
                """UPDATE news SET estimated_reading_time = 
                   CASE 
                       WHEN LENGTH(COALESCE(content_en, '')) > 0 
                       THEN MAX(1, ROUND(LENGTH(REPLACE(content_en, '<', ' <')) / 1000.0))
                       ELSE 1 
                   END 
                   WHERE estimated_reading_time IS NULL""",
            ]
            
            for query in update_queries:
                try:
                    cursor.execute(query)
                    print(f"✓ Updated default values")
                except sqlite3.Error as e:
                    print(f"✗ Error updating defaults: {e}")
        
        # Commit changes
        conn.commit()
        
        print(f"\n✅ Migration completed successfully!")
        print(f"Added {len(added_columns)} new columns to the news table.")
        
        if added_columns:
            print("\nNew columns added:")
            for col in added_columns:
                print(f"  - {col}")
        else:
            print("All columns already exist in the database.")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def verify_migration():
    """Verify that all columns were added successfully"""
    
    db_path = 'instance/emdad_global.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get table schema
        cursor.execute("PRAGMA table_info(news)")
        columns = cursor.fetchall()
        
        print("\n📋 Current news table schema:")
        print("-" * 50)
        for column in columns:
            print(f"  {column[1]} ({column[2]})")
        
        print(f"\nTotal columns: {len(columns)}")
        
        # Check for specific new columns
        column_names = [col[1] for col in columns]
        required_columns = [
            'focus_keyword_en', 'focus_keyword_ar',
            'seo_title_en', 'seo_title_ar',
            'og_title_en', 'twitter_title_en',
            'article_type', 'estimated_reading_time'
        ]
        
        missing_columns = [col for col in required_columns if col not in column_names]
        
        if missing_columns:
            print(f"\n⚠️  Missing columns: {', '.join(missing_columns)}")
            return False
        else:
            print("\n✅ All required columns are present!")
            return True
            
    except sqlite3.Error as e:
        print(f"❌ Error verifying migration: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔄 News Table Migration Script")
    print("=" * 40)
    
    # Run migration
    success = migrate_database()
    
    if success:
        # Verify migration
        print("\n🔍 Verifying migration...")
        verify_migration()
        
        print("\n🎉 Migration completed! You can now restart your Flask application.")
        print("\n💡 Next steps:")
        print("   1. Restart your Flask application")
        print("   2. Test the news form with new features")
        print("   3. Check that existing news articles still work")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure the Flask app is not running")
        print("   2. Check database file permissions")
        print("   3. Backup your database before running again")
