-- TechMart - Update product images (for a database that already exists)
-- Open a New Query in SSMS, run this whole code (F5).
-- It only updates the Image column of the 12 sample products.
-- No product, order or user is deleted.

USE TechMartDB;
GO

UPDATE Products SET Image = 'galaxy-a55.png' WHERE Id = 1;
UPDATE Products SET Image = 'iphone-13.jpg' WHERE Id = 2;
UPDATE Products SET Image = 'redmi-note13.png' WHERE Id = 3;
UPDATE Products SET Image = 'hp-pavilion.jpg' WHERE Id = 4;
UPDATE Products SET Image = 'lenovo-ideapad.jpg' WHERE Id = 5;
UPDATE Products SET Image = 'dell-inspiron.webp' WHERE Id = 6;
UPDATE Products SET Image = 'airpods-pro.webp' WHERE Id = 7;
UPDATE Products SET Image = 'galaxy-buds.webp' WHERE Id = 8;
UPDATE Products SET Image = 'jbl-headphones.jpg' WHERE Id = 9;
UPDATE Products SET Image = 'apple-watch.jpg' WHERE Id = 10;
UPDATE Products SET Image = 'galaxy-watch.jpg' WHERE Id = 11;
UPDATE Products SET Image = 'mi-band.png' WHERE Id = 12;
GO

-- Check: run this query to verify
SELECT Id, Name, Image FROM Products;
