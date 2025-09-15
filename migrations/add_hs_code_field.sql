-- Migration: Add HS Code field to products table
-- Date: 2025-01-15
-- Description: Add hs_code field to store Harmonized System codes for products

-- Add hs_code column to product table
ALTER TABLE product ADD COLUMN hs_code VARCHAR(20);

-- Add index for better performance on HS code searches
CREATE INDEX idx_product_hs_code ON product(hs_code);

-- Add comment to document the field
COMMENT ON COLUMN product.hs_code IS 'Harmonized System (HS) code for customs and trade classification';
