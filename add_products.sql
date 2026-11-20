-- TechMart - Add 48 more products (products 13 to 60)
-- Run this in SSMS in a New Query (F5) on the database TechMartDB.
-- Use this file if you already created the database with techmart_sqlserver.sql.
-- Do NOT run techmart_sqlserver.sql again - it is only for a fresh database.
--
-- SAFE: This script only ADDS new products.
-- There is no DROP, DELETE or UPDATE in it.
-- Your existing products (Ids 1-12), users, orders and other databases
-- (college, QuizManagementDB, AdventureWorks) will stay exactly as they are.
-- After this, TechMartDB will have 60 products in total (15 in each category).

USE TechMartDB;
GO

-- New Mobiles (CategoryId 1) - products 13 to 24
INSERT INTO Products (CategoryId, Name, Description, Price, OldPrice, Image, Stock) VALUES
(1, 'Samsung Galaxy S24', '8GB RAM, 256GB Storage, 50MP Camera', 285000, 310000, 'galaxy-s24.webp', 12),
(1, 'iPhone 15', '128GB Storage, A16 Bionic Chip, 48MP Camera', 340000, 365000, 'iphone-15.webp', 10),
(1, 'Google Pixel 8', '8GB RAM, 128GB Storage, Google Tensor G3 Chip', 240000, 260000, 'pixel-8.jpg', 9),
(1, 'OnePlus 12', '12GB RAM, 256GB Storage, Snapdragon 8 Gen 3', 230000, 250000, 'oneplus-12.jpg', 8),
(1, 'Vivo V30', '12GB RAM, 256GB Storage, 50MP Portrait Camera', 145000, 160000, 'vivo-v30.jpg', 14),
(1, 'Oppo Reno 11', '12GB RAM, 256GB Storage, 50MP Camera', 155000, 170000, 'oppo-reno11.jpg', 11),
(1, 'Infinix Note 40', '8GB RAM, 256GB Storage, 70W Fast Charging', 72000, 80000, 'infinix-note40.jpg', 18),
(1, 'Tecno Camon 30', '8GB RAM, 256GB Storage, 50MP Camera', 78000, 88000, 'tecno-camon30.webp', 16),
(1, 'Realme 12 Pro', '8GB RAM, 256GB Storage, 64MP Periscope Camera', 115000, 128000, 'realme-12pro.jpg', 13),
(1, 'Samsung Galaxy A35', '8GB RAM, 128GB Storage, 50MP Camera, 5000mAh Battery', 135000, 148000, 'galaxy-a35.jpg', 15),
(1, 'iPhone 12', '64GB Storage, A14 Bionic Chip, Dual Camera', 165000, 180000, 'iphone-12.jpg', 7),
(1, 'Xiaomi Redmi 12', '4GB RAM, 128GB Storage, 50MP Camera', 48000, 55000, 'redmi-12.jpg', 22);
GO

-- New Laptops (CategoryId 2) - products 25 to 36
INSERT INTO Products (CategoryId, Name, Description, Price, OldPrice, Image, Stock) VALUES
(2, 'MacBook Air M2', 'Apple M2 Chip, 8GB RAM, 256GB SSD', 385000, 410000, 'macbook-air.jpg', 6),
(2, 'Asus VivoBook 15', 'Intel Core i5, 8GB RAM, 512GB SSD', 155000, 170000, 'asus-vivobook.png', 10),
(2, 'Acer Aspire 5', 'Intel Core i5, 8GB RAM, 512GB SSD', 145000, 158000, 'acer-aspire5.jpg', 9),
(2, 'HP 15s', 'Intel Core i5, 8GB RAM, 512GB SSD', 135000, 148000, 'hp-15s.jpg', 12),
(2, 'Lenovo ThinkPad E14', 'Intel Core i5, 16GB RAM, 512GB SSD', 245000, 265000, 'thinkpad-e14.jpg', 7),
(2, 'Dell XPS 13', 'Intel Core i7, 16GB RAM, 512GB SSD', 425000, 450000, 'dell-xps13.jpg', 5),
(2, 'Asus ROG Strix G16', 'Intel Core i9, RTX 4060, 16GB RAM, 1TB SSD', 485000, 520000, 'rog-strix-g16.jpg', 6),
(2, 'HP Victus 15', 'AMD Ryzen 5, GTX 1650, 8GB RAM, 512GB SSD', 265000, 285000, 'hp-victus15.jpg', 8),
(2, 'Lenovo Legion 5', 'AMD Ryzen 7, RTX 4060, 16GB RAM, 512GB SSD', 395000, 425000, 'lenovo-legion5.jpg', 6),
(2, 'Samsung Galaxy Book 4', 'Intel Core i7, 16GB RAM, 512GB SSD', 295000, 320000, 'galaxy-book4.jpg', 7),
(2, 'Microsoft Surface Laptop 5', 'Intel Core i7, 16GB RAM, 512GB SSD', 365000, 390000, 'surface-laptop5.jpg', 5),
(2, 'Dell Latitude 5430', 'Intel Core i5, 8GB RAM, 256GB SSD', 315000, 340000, 'dell-latitude5430.jpg', 8);
GO

-- New Headphones (CategoryId 3) - products 37 to 48
INSERT INTO Products (CategoryId, Name, Description, Price, OldPrice, Image, Stock) VALUES
(3, 'Sony WH-1000XM5', 'Industry Leading Noise Cancellation, 30 Hours Battery', 95000, 110000, 'sony-wh1000xm5.jpg', 14),
(3, 'JBL Tune 510BT', 'On-ear Bluetooth, 40 Hours Battery Life', 15000, 18000, 'jbl-tune510bt.jpg', 20),
(3, 'Soundcore Life Q30', 'Hybrid Active Noise Cancellation, 40 Hours Playtime', 25000, 29000, 'soundcore-q30.jpg', 16),
(3, 'Sony WF-1000XM5', 'True Wireless Earbuds, Best Noise Cancellation', 75000, 85000, 'sony-wf1000xm5.jpg', 12),
(3, 'Samsung Galaxy Buds FE', 'Wireless Earbuds, Active Noise Cancellation', 22000, 26000, 'galaxy-buds-fe.jpg', 18),
(3, 'AirPods Max', 'Over-ear, Active Noise Cancellation, Spatial Audio', 165000, 180000, 'airpods-max.jpg', 6),
(3, 'Boat Rockerz 450', 'On-ear Bluetooth, 15 Hours Playtime', 9000, 12000, 'boat-rockerz450.jpg', 25),
(3, 'Anker Soundcore Liberty 4', 'True Wireless Earbuds, Hi-Res Audio', 32000, 38000, 'soundcore-liberty4.jpg', 15),
(3, 'Skullcandy Crusher Evo', 'Over-ear, Sensory Bass, 40 Hours Battery', 45000, 52000, 'skullcandy-crusher.jpg', 10),
(3, 'JBL Tune 720BT', 'Over-ear Bluetooth, 76 Hours Battery Life', 28000, 33000, 'jbl-tune720bt.jpg', 17),
(3, 'Sony WH-CH720N', 'Noise Cancelling Over-ear, 35 Hours Battery', 38000, 45000, 'sony-wh-ch720n.jpg', 13),
(3, 'Oppo Enco Air 3', 'True Wireless Earbuds, 13mm Driver', 12000, 15000, 'oppo-enco-air3.jpg', 21);
GO

-- New Smartwatch (CategoryId 4) - products 49 to 60
INSERT INTO Products (CategoryId, Name, Description, Price, OldPrice, Image, Stock) VALUES
(4, 'Apple Watch Series 9', 'Fitness Tracking, Always-On Display', 145000, 160000, 'apple-watch-s9.jpg', 11),
(4, 'Samsung Galaxy Watch 5', 'AMOLED Display, Health Tracking', 65000, 72000, 'galaxy-watch5.jpg', 13),
(4, 'Amazfit GTS 4', 'AMOLED Display, 150+ Sport Modes', 55000, 62000, 'amazfit-gts4.jpg', 14),
(4, 'Huawei Watch GT 4', 'AMOLED Display, 14 Days Battery Life', 85000, 95000, 'huawei-watch-gt4.jpg', 9),
(4, 'Fitbit Versa 4', 'Fitness Tracking, 40+ Exercise Modes', 78000, 88000, 'fitbit-versa4.webp', 10),
(4, 'Garmin Forerunner 55', 'GPS Running Watch, 20 Hours Battery', 68000, 76000, 'garmin-forerunner55.jpg', 8),
(4, 'Apple Watch Ultra 2', 'Titanium Case, 36 Hours Battery Life', 265000, 290000, 'apple-watch-ultra2.jpg', 6),
(4, 'Xiaomi Watch S3', 'AMOLED Display, 15 Days Battery Life', 48000, 55000, 'xiaomi-watch-s3.png', 15),
(4, 'Noise ColorFit Pro 5', 'Bluetooth Calling, 1.85 inch Display', 9000, 12000, 'noise-colorfit-pro5.jpg', 24),
(4, 'Fire-Boltt Ninja Call Pro', 'Bluetooth Calling, 120+ Sport Modes', 7500, 10000, 'fire-boltt-ninja.webp', 28),
(4, 'Haylou Solar Plus RT3', 'AMOLED Display, Bluetooth Calling', 14000, 17000, 'haylou-solar-rt3.jpg', 19),
(4, 'Oppo Watch X', 'AMOLED Display, Wear OS, Health Tracking', 95000, 105000, 'oppo-watch-x.png', 7);
GO

-- Verify: this should show 60 products in total (15 in each category)
SELECT COUNT(*) AS TotalProducts FROM Products;
SELECT CategoryId, COUNT(*) AS ProductsInCategory FROM Products GROUP BY CategoryId ORDER BY CategoryId;
