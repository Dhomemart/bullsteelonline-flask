-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 192.168.1.29    Database: metalsheet5
-- ------------------------------------------------------
-- Server version	5.5.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `productgroup`
--

DROP TABLE IF EXISTS `productgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productgroup` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `code` varchar(20) DEFAULT '-',
  `name` varchar(100) DEFAULT '-',
  `raw` int(1) DEFAULT '0',
  `pc1` double(10,2) DEFAULT '0.00',
  `pc2` double(10,2) DEFAULT '0.00',
  `pc3` double(10,2) DEFAULT '0.00',
  `pc4` double(10,2) DEFAULT '0.00',
  `amt1` double(10,2) DEFAULT '0.00',
  `amt2` double(10,2) DEFAULT '0.00',
  `amt3` double(10,2) DEFAULT '0.00',
  `amt4` double(10,2) DEFAULT '0.00',
  `markdown` int(1) DEFAULT '0',
  `pricemarkup` int(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `code` (`code`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productgroup`
--

LOCK TABLES `productgroup` WRITE;
/*!40000 ALTER TABLE `productgroup` DISABLE KEYS */;
INSERT INTO `productgroup` VALUES (1,'001','เมทัลชีท',1,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0),(2,'002','ลอนตรง สต็อค',0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0),(3,'003','ครอบข้าง สต็อค',0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0),(4,'004','ครอบจั่ว สต็อค',0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0),(5,'005','ครอบชนผนัง สต็อค',0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0),(6,'006','แผ่นเรียบ สต็อค',0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0),(7,'007','แผ่นเรียบ รีดครอบ',0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0),(8,'008','สินค้ามีตำหนิ',0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0),(9,'009','ค่าบริการ ',0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0);
/*!40000 ALTER TABLE `productgroup` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-28 23:55:01
