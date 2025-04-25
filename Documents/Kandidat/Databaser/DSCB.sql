DROP TABLE IF EXISTS Battles; 

CREATE TABLE `Battles`(
    `name` varchar(20),
    `battledate` char(10)
);

INSERT INTO Battles VALUES ('North Atlantic', '1941-05-24');
INSERT INTO Battles VALUES ('Guadalcanal','1942-11-15');
INSERT INTO Battles VALUES ('North Cape','1943-02-26');
INSERT INTO Battles VALUES ('Suriago Strait','1944-10-25');

DROP TABLE IF EXISTS Classes; 

CREATE TABLE `Classes`(
    `class` varchar(20),
    `type` varchar(2),
    `country` varchar(20),
    `numGuns` int,
    `bore` int,
    `displacement` int
);

INSERT INTO Classes VALUES ('Bismarck','bb','Germany',8,15,42000);
INSERT INTO Classes VALUES ('Iowa','bb','USA',9,16,46000);
INSERT INTO Classes VALUES ('Kongo','bc','Japan',8,14,32000);
INSERT INTO Classes VALUES ('North Carolina','bb','USA',9,16,37000);
INSERT INTO Classes VALUES ('Renown','bc','Gt. Britain',6,15,32000);
INSERT INTO Classes VALUES ('Revenge','bb','Gt. Britain',8,15,29000);
INSERT INTO Classes VALUES ('Tennessee','bb','USA',12,14,32000);
INSERT INTO Classes VALUES ('Yamato','bb','Japan',9,18,65000);

DROP TABLE IF EXISTS Example; 

CREATE TABLE `Example`(
    `a` int,
    `b` int,
    `c` int,
    `x` int,
    `y` int,
    `z` int,
    `s` varchar(20),
    `t` varchar(20)
);

INSERT INTO Example VALUES (0, 0, 0, 1, 2, 3, 'Donald', 'Duck');
INSERT INTO Example VALUES (0, 0, 1, 4, 5, 6, 'Roger', 'Rabbit');
INSERT INTO Example VALUES (0, 1, 0, 7, 8, 9, 'Popeye', 'Sailorman');
INSERT INTO Example VALUES (0, 1, 1, 11, 13, 17, 'Mickey', 'Mouse');
INSERT INTO Example VALUES (1, 0, 0, 19, 23, 29, 'Peter', 'Pan');
INSERT INTO Example VALUES (1, 0, 1, 31, 37, 41, 'Bugs', 'Bunny');
INSERT INTO Example VALUES (1, 1, 0, 43, 47, 51, 'Gyro', 'Gearloose');
INSERT INTO Example VALUES (1, 1, 1, 53, 57, 59, 'Uncle', 'Scrooge');

DROP TABLE IF EXISTS Laptop;

CREATE TABLE `Laptop`(
    `model` varchar(4),
    `speed` int,
    `ram` int,
    `hd` int,
    `screen` float(5),
    `price` int
);

INSERT INTO Laptop VALUES ('2001', 700, 64, 5, 12.1, 1448);
INSERT INTO Laptop VALUES ('2002', 800, 96, 10, 15.1, 2584);
INSERT INTO Laptop VALUES ('2003', 850, 64, 10, 15.1, 2738);
INSERT INTO Laptop VALUES ('2004', 550, 32, 5, 12.1, 999);
INSERT INTO Laptop VALUES ('2005', 600, 64, 6, 12.1, 2399);
INSERT INTO Laptop VALUES ('2006', 800, 96, 20, 15.7, 2999);
INSERT INTO Laptop VALUES ('2007', 850, 128, 20, 15.0, 3099);
INSERT INTO Laptop VALUES ('2008', 650, 64, 10, 12.1, 1249);
INSERT INTO Laptop VALUES ('2009', 750, 256, 20, 15.1, 2599);
INSERT INTO Laptop VALUES ('2010', 366, 64, 10, 12.1, 1499);

DROP TABLE IF EXISTS Movie; 

CREATE TABLE `Movie`(
    `title` varchar(25),
    `year` int,
    `length` int,
    `inColor` int,
    `studioName` varchar(15),
    `producerC` varchar(3)
);

INSERT INTO Movie VALUES ('Pretty Woman', 1990, 119, 1, 'Disney', '999');
INSERT INTO Movie VALUES ('The Man Who Wasn''t There', 2001, 116, 0, 'USA Entertainm.', '777');
INSERT INTO Movie VALUES ('Logan''s run', 1976, NULL, 1, '', '888');
INSERT INTO Movie VALUES ('Star Wars', 1977, 124, 1, 'Fox', '555');
INSERT INTO Movie VALUES ('Empire Strikes Back', 1980, 111, 1, 'Fox', '555');
INSERT INTO Movie VALUES ('Star Trek', 1979, 132, 1, 'Paramount', '444');
INSERT INTO Movie VALUES ('Star Trek: Nemesis', 2002, 116, 1, 'Paramount', '321');
INSERT INTO Movie VALUES ('Terms of Endearment', 1983, 132, 1, 'MGM', '123');
INSERT INTO Movie VALUES ('The Usual Suspects', 1995, 106, 1, 'MGM', '999');
INSERT INTO Movie VALUES ('Gone With the Wind', 1938, 238, 1, 'MGM', '123');

DROP TABLE IF EXISTS MovieExec; 

CREATE TABLE `MovieExec`(
    `name` varchar(30),
    `address` varchar(30),
    `cert` int,
    `netWorth` int
);

INSERT INTO MovieExec VALUES ('George Lucas', 'Oak Rd.', 555, 200000000);
INSERT INTO MovieExec VALUES ('Ted Turner', 'Turner Av.', 333, 125000000);
INSERT INTO MovieExec VALUES ('Stephen Spielberg', '123 ET road', 222, 100000000);
INSERT INTO MovieExec VALUES ('Merv Griffin', 'Riot Rd.', 199, 112000000);
INSERT INTO MovieExec VALUES ('Calvin Coolidge', 'Fast Lane', 123, 20000000);

DROP TABLE IF EXISTS MovieStar; 

CREATE TABLE `MovieStar`(
    `name` varchar(30),
    `address` varchar(30),
    `gender` varchar(1),
    `birthdate` varchar(10)
);

INSERT INTO MovieStar VALUES ('Jane Fonda', 'Turner Av.', 'F', '7/7/77');
INSERT INTO MovieStar VALUES ('Alec Baldwin', 'Baldwin Av.', 'M', '6/7/77');
INSERT INTO MovieStar VALUES ('Kim Basinger', 'Baldwin Av.', 'F', '5/7/79');
INSERT INTO MovieStar VALUES ('Harrison Ford', 'Prefect Rd.', 'M', '5/5/55');
INSERT INTO MovieStar VALUES ('Debra Winger', 'A way', 'F', '5/6/78');
INSERT INTO MovieStar VALUES ('Jack Nicholson', 'X path', 'M', '5/5/49');

DROP TABLE IF EXISTS Outcomes; 

CREATE TABLE `Outcomes`(
    `ship` varchar(20),
    `battle` varchar(20),
    `result` varchar(10)
);

INSERT INTO Outcomes VALUES ('Bismarck','North Atlantic','sunk');
INSERT INTO Outcomes VALUES ('California','Suriago Strait','ok');
INSERT INTO Outcomes VALUES ('Duke of York','North Cape','ok');
INSERT INTO Outcomes VALUES ('Fuso','Suriago Strait','sunk');
INSERT INTO Outcomes VALUES ('Hood','North Atlantic','sunk');
INSERT INTO Outcomes VALUES ('King George V','North Atlantic','ok');
INSERT INTO Outcomes VALUES ('Kirishima','Guadalcanal','sunk');
INSERT INTO Outcomes VALUES ('Prince of Wales','North Atlantic','damaged');
INSERT INTO Outcomes VALUES ('Rodney','North Atlantic','ok');
INSERT INTO Outcomes VALUES ('Scharnhorst','North Cape','sunk');
INSERT INTO Outcomes VALUES ('South Dakota','Guadalcanal','damaged');
INSERT INTO Outcomes VALUES ('Tennessee','Suriago Strait','ok');
INSERT INTO Outcomes VALUES ('Washington','Guadalcanal','ok');
INSERT INTO Outcomes VALUES ('West Virginia','Suriago Strait','ok');
INSERT INTO Outcomes VALUES ('Yamashiro','Suriago Strait','sunk');

DROP TABLE IF EXISTS PC; 

CREATE TABLE `PC`(
    `model` varchar(4),
    `speed` int,
    `ram` int,
    `hd` int,
    `rd` varchar(10),
    `price` int
);

INSERT INTO PC VALUES ('1001', 700, 64, 10, '48xCD', 799);
INSERT INTO PC VALUES ('1002', 1500, 128, 60, '12xDVD', 2499);
INSERT INTO PC VALUES ('1003', 866, 128, 20, '8xDVD', 1999);
INSERT INTO PC VALUES ('1004', 866, 64, 10, '12xDVD', 999);
INSERT INTO PC VALUES ('1005', 1000, 128, 20, '12xDVD', 1499);
INSERT INTO PC VALUES ('1006', 1300, 256, 40, '16xDVD', 2119);
INSERT INTO PC VALUES ('1007', 1400, 128, 80, '12xDVD', 2299);
INSERT INTO PC VALUES ('1008', 700, 64, 30, '24xCD', 999);
INSERT INTO PC VALUES ('1009', 1200, 128, 80, '16xDVD', 1699);
INSERT INTO PC VALUES ('1010', 750, 64, 30, '40xCD', 699);
INSERT INTO PC VALUES ('1011', 1100, 128, 60, '16xDVD', 1299);
INSERT INTO PC VALUES ('1012', 350, 64, 7, '48xCD', 799);
INSERT INTO PC VALUES ('1013', 733, 256, 60, '12xDVD', 2499);

DROP TABLE IF EXISTS Printer; 

CREATE TABLE `Printer`(
    `model` varchar(4),
    `color` int,
    `type` varchar(15),
    `price` int
);

INSERT INTO Printer VALUES ('3001', 1, 'ink-jet', 231);
INSERT INTO Printer VALUES ('3002', 1, 'ink-jet', 267);
INSERT INTO Printer VALUES ('3003', 0, 'laser', 390);
INSERT INTO Printer VALUES ('3004', 1, 'ink-jet', 439);
INSERT INTO Printer VALUES ('3005', 1, 'bubble', 200);
INSERT INTO Printer VALUES ('3006', 1, 'laser', 1999);
INSERT INTO Printer VALUES ('3007', 0, 'laser', 350);

DROP TABLE IF EXISTS Product; 

CREATE TABLE `Product`(
    `id` int,
    `maker` varchar(1),
    `model` varchar(4),
    `type` varchar(10)
);

INSERT INTO Product VALUES (1,'A', '1001', 'pc');
INSERT INTO Product VALUES (2,'A', '1002', 'pc');
INSERT INTO Product VALUES (3,'A', '1003', 'pc');
INSERT INTO Product VALUES (4,'A', '2004', 'laptop');
INSERT INTO Product VALUES (5,'A', '2005', 'laptop');
INSERT INTO Product VALUES (6,'A', '2006', 'laptop');
INSERT INTO Product VALUES (7,'B', '1004', 'pc');
INSERT INTO Product VALUES (8,'B', '1005', 'pc');
INSERT INTO Product VALUES (9,'B', '1006', 'pc');
INSERT INTO Product VALUES (10,'B', '2001', 'laptop');
INSERT INTO Product VALUES (11,'B', '2002', 'laptop');
INSERT INTO Product VALUES (12,'B', '2003', 'laptop');
INSERT INTO Product VALUES (13,'C', '1007', 'pc');
INSERT INTO Product VALUES (14,'C', '1008', 'pc');
INSERT INTO Product VALUES (15,'C', '2008', 'laptop');
INSERT INTO Product VALUES (16,'C', '2009', 'laptop');
INSERT INTO Product VALUES (17,'C', '3002', 'printer');
INSERT INTO Product VALUES (18,'C', '3003', 'printer');
INSERT INTO Product VALUES (19,'C', '3006', 'printer');
INSERT INTO Product VALUES (20,'D', '1009', 'pc');
INSERT INTO Product VALUES (21,'D', '1010', 'pc');
INSERT INTO Product VALUES (22,'D', '1011', 'pc');
INSERT INTO Product VALUES (23,'D', '2007', 'laptop');
INSERT INTO Product VALUES (24,'E', '1012', 'pc');
INSERT INTO Product VALUES (25,'E', '1013', 'pc');
INSERT INTO Product VALUES (26,'E', '2010', 'laptop');
INSERT INTO Product VALUES (27,'F', '3001', 'printer');
INSERT INTO Product VALUES (28,'F', '3004', 'printer');
INSERT INTO Product VALUES (29,'G', '3005', 'printer');
INSERT INTO Product VALUES (30,'H', '3007', 'printer');

DROP TABLE IF EXISTS Sales;

CREATE TABLE `Sales`(
    `salesmanID` int,
    `productID` int,
    `day` char(10)
);

INSERT INTO Sales VALUES (1,6,'2002-10-21');
INSERT INTO Sales VALUES (1,11,'2002-07-12');
INSERT INTO Sales VALUES (1,2,'2003-04-30');
INSERT INTO Sales VALUES (1,23,'2003-02-11');
INSERT INTO Sales VALUES (2,15,'2004-09-05');
INSERT INTO Sales VALUES (2,11,'2002-08-07');
INSERT INTO Sales VALUES (2,9,'2002-12-14');
INSERT INTO Sales VALUES (2,27,'2003-11-15');
INSERT INTO Sales VALUES (3,13,'2004-01-25');
INSERT INTO Sales VALUES (3,4,'2003-03-05');
INSERT INTO Sales VALUES (3,22,'2002-09-17');
INSERT INTO Sales VALUES (3,30,'2004-04-01');
INSERT INTO Sales VALUES (3,22,'2004-09-02');
INSERT INTO Sales VALUES (3,23,'2003-04-07');
INSERT INTO Sales VALUES (3,2,'2002-03-14');
INSERT INTO Sales VALUES (4,23,'2001-02-25');
INSERT INTO Sales VALUES (4,1,'2002-10-32');
INSERT INTO Sales VALUES (4,5,'2003-11-17');
INSERT INTO Sales VALUES (1,2,'2002-10-21');
INSERT INTO Sales VALUES (1,21,'2002-07-12');
INSERT INTO Sales VALUES (1,20,'2003-04-30');
INSERT INTO Sales VALUES (1,19,'2003-02-11');
INSERT INTO Sales VALUES (2,28,'2004-09-05');
INSERT INTO Sales VALUES (2,27,'2002-08-07');
INSERT INTO Sales VALUES (2,29,'2002-12-14');
INSERT INTO Sales VALUES (2,10,'2003-11-15');
INSERT INTO Sales VALUES (3,3,'2004-01-25');
INSERT INTO Sales VALUES (3,2,'2003-03-05');
INSERT INTO Sales VALUES (3,1,'2002-09-17');
INSERT INTO Sales VALUES (3,23,'2004-04-01');
INSERT INTO Sales VALUES (3,17,'2004-09-02');
INSERT INTO Sales VALUES (3,24,'2003-04-07');
INSERT INTO Sales VALUES (3,9,'2002-03-14');
INSERT INTO Sales VALUES (4,23,'2001-02-25');
INSERT INTO Sales VALUES (4,11,'2002-10-32');
INSERT INTO Sales VALUES (4,4,'2003-11-17');

DROP TABLE IF EXISTS Salesmen;

CREATE TABLE `Salesmen`(
    `salesmanID` int,
    `name` varchar(20),
    `salary` int
);

INSERT INTO Salesmen VALUES (1,'Benny Boom',60000);
INSERT INTO Salesmen VALUES (2,'Charlie Chap',40000);
INSERT INTO Salesmen VALUES (3,'Danny Doom',100000);
INSERT INTO Salesmen VALUES (4,'Al Capslock',50000);

DROP TABLE IF EXISTS Ships; 

CREATE TABLE `Ships`(
    `name` varchar(20),
    `class` varchar(20),
    `launched` int
);

INSERT INTO Ships VALUES ('California','Tennessee',1921);
INSERT INTO Ships VALUES ('Haruna','Kongo',1915);
INSERT INTO Ships VALUES ('Hiei','Kongo',1914);
INSERT INTO Ships VALUES ('Iowa','Iowa',1943);
INSERT INTO Ships VALUES ('Kirishima','Kongo',1915);
INSERT INTO Ships VALUES ('Kongo','Kongo',1913);
INSERT INTO Ships VALUES ('Missouri','Iowa',1944);
INSERT INTO Ships VALUES ('Musashi','Yamato',1942);
INSERT INTO Ships VALUES ('New Jersey','Iowa',1943);
INSERT INTO Ships VALUES ('North Carolina','North Carolina',1941);
INSERT INTO Ships VALUES ('Ramillies','Revenge',1917);
INSERT INTO Ships VALUES ('Renown','Renown',1916);
INSERT INTO Ships VALUES ('Repulse','Renown',1916);
INSERT INTO Ships VALUES ('Resolution','Revenge',1916);
INSERT INTO Ships VALUES ('Revenge','Revenge',1916);
INSERT INTO Ships VALUES ('Royal Oak','Revenge',1916);
INSERT INTO Ships VALUES ('Royal Sovereign','Revenge',1916);
INSERT INTO Ships VALUES ('Tennessee','Tennessee',1920);
INSERT INTO Ships VALUES ('Washington','North Carolina',1941);
INSERT INTO Ships VALUES ('Wisconsin','Iowa',1944);
INSERT INTO Ships VALUES ('Yamato','Yamato',1941);

DROP TABLE IF EXISTS StarsIn; 

CREATE TABLE `StarsIn`(
    `movieTitle` varchar(30),
    `movieYear` int,
    `starName` varchar(30)
);

INSERT INTO StarsIn VALUES ('Star Wars', 1977, 'Carrie Fisher');
INSERT INTO StarsIn VALUES ('Star Wars', 1977, 'Mark Hamill');
INSERT INTO StarsIn VALUES ('Star Wars', 1977, 'Harrison Ford');
INSERT INTO StarsIn VALUES ('Empire Strikes Back', 1980, 'Harrison Ford');
INSERT INTO StarsIn VALUES ('The Usual Suspects', 1995, 'Kevin Spacey');
INSERT INTO StarsIn VALUES ('Terms of Endearment', 1983, 'Debra Winger');
INSERT INTO StarsIn VALUES ('Terms of Endearment', 1983, 'Jack Nicholson');

DROP TABLE IF EXISTS Studio; 

CREATE TABLE `Studio`(
    `name` varchar(30),
    `address` varchar(30),
    `presC` int
);

INSERT INTO Studio VALUES ('MGM','MGM Boulevard', 123);
