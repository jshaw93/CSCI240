-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
--
-- Host: localhost    Database: project
-- ------------------------------------------------------
-- Server version	8.0.34-0ubuntu0.23.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Favorites`
--

DROP TABLE IF EXISTS `Favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Favorites` (
  `FavoriteID` int NOT NULL AUTO_INCREMENT,
  `ItemID` smallint NOT NULL,
  PRIMARY KEY (`FavoriteID`,`ItemID`),
  KEY `ItemIDFK` (`ItemID`),
  CONSTRAINT `ItemIDFK` FOREIGN KEY (`ItemID`) REFERENCES `Item` (`ItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Favorites`
--

LOCK TABLES `Favorites` WRITE;
/*!40000 ALTER TABLE `Favorites` DISABLE KEYS */;
INSERT INTO `Favorites` VALUES (1,2),(1,1319);
/*!40000 ALTER TABLE `Favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Item`
--

DROP TABLE IF EXISTS `Item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Item` (
  `ItemID` smallint NOT NULL,
  `Membs` tinyint(1) NOT NULL,
  `Alch` int unsigned NOT NULL,
  PRIMARY KEY (`ItemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Item`
--

LOCK TABLES `Item` WRITE;
/*!40000 ALTER TABLE `Item` DISABLE KEYS */;
INSERT INTO `Item` VALUES (2,1,3),(440,0,10),(451,0,1920),(453,0,27),(1319,0,38400),(2353,0,60),(2363,0,3000);
/*!40000 ALTER TABLE `Item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ItemRecipe`
--

DROP TABLE IF EXISTS `ItemRecipe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ItemRecipe` (
  `ItemRecipeID` smallint unsigned NOT NULL,
  `ItemID` smallint NOT NULL,
  `Quantity` smallint unsigned NOT NULL,
  PRIMARY KEY (`ItemRecipeID`,`ItemID`),
  KEY `ItemID` (`ItemID`),
  CONSTRAINT `ItemRecipe_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `Item` (`ItemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ItemRecipe`
--

LOCK TABLES `ItemRecipe` WRITE;
/*!40000 ALTER TABLE `ItemRecipe` DISABLE KEYS */;
INSERT INTO `ItemRecipe` VALUES (1,2353,1),(2,2363,3),(3,440,1),(3,453,2),(4,451,1),(4,453,8);
/*!40000 ALTER TABLE `ItemRecipe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Player`
--

DROP TABLE IF EXISTS `Player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Player` (
  `PlayerID` smallint NOT NULL AUTO_INCREMENT,
  `Name` varchar(20) NOT NULL,
  `FavoriteID` int DEFAULT NULL,
  PRIMARY KEY (`PlayerID`),
  KEY `FavoriteID` (`FavoriteID`),
  CONSTRAINT `Player_ibfk_1` FOREIGN KEY (`FavoriteID`) REFERENCES `Favorites` (`FavoriteID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Player`
--

LOCK TABLES `Player` WRITE;
/*!40000 ALTER TABLE `Player` DISABLE KEYS */;
/*!40000 ALTER TABLE `Player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PlayerSkill`
--

DROP TABLE IF EXISTS `PlayerSkill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PlayerSkill` (
  `PlayerID` smallint NOT NULL,
  `SkillLvl` tinyint unsigned NOT NULL,
  `SkillName` varchar(255) NOT NULL,
  PRIMARY KEY (`PlayerID`,`SkillName`),
  KEY `SkillName` (`SkillName`),
  CONSTRAINT `PlayerSkill_ibfk_1` FOREIGN KEY (`SkillName`) REFERENCES `Skill` (`SkillName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PlayerSkill`
--

LOCK TABLES `PlayerSkill` WRITE;
/*!40000 ALTER TABLE `PlayerSkill` DISABLE KEYS */;
INSERT INTO `PlayerSkill` VALUES (1,99,'Smithing');
/*!40000 ALTER TABLE `PlayerSkill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Recipe`
--

DROP TABLE IF EXISTS `Recipe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Recipe` (
  `RecipeID` int unsigned NOT NULL AUTO_INCREMENT,
  `ItemCreatedID` smallint NOT NULL,
  `RecipeName` varchar(30) NOT NULL,
  `AmtProduced` smallint unsigned NOT NULL,
  `ItemRecipeID` smallint unsigned NOT NULL,
  `SkillLvl` tinyint unsigned NOT NULL,
  `SkillName` varchar(255) NOT NULL,
  PRIMARY KEY (`RecipeID`),
  KEY `ItemCreatedIDFK` (`ItemCreatedID`),
  KEY `SkillNameFK` (`SkillName`),
  KEY `ItemRecipeIDFK` (`ItemRecipeID`),
  CONSTRAINT `ItemCreatedIDFK` FOREIGN KEY (`ItemCreatedID`) REFERENCES `Item` (`ItemID`),
  CONSTRAINT `SkillNameFK` FOREIGN KEY (`SkillName`) REFERENCES `Skill` (`SkillName`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Recipe`
--

LOCK TABLES `Recipe` WRITE;
/*!40000 ALTER TABLE `Recipe` DISABLE KEYS */;
INSERT INTO `Recipe` VALUES (1,2,'Cannonballs',4,1,32,'Smithing'),(2,1319,'Rune2h',1,2,99,'Smithing'),(3,2353,'Steel Bar',1,3,30,'Smithing'),(4,2363,'Runite Bar',1,4,85,'Smithing');
/*!40000 ALTER TABLE `Recipe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Skill`
--

DROP TABLE IF EXISTS `Skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Skill` (
  `SkillName` varchar(255) NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `Image` longblob,
  PRIMARY KEY (`SkillName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Skill`
--

LOCK TABLES `Skill` WRITE;
/*!40000 ALTER TABLE `Skill` DISABLE KEYS */;
INSERT INTO `Skill` VALUES ('Cooking','A skill concerning the creation of food items',NULL),('Herblore','A skill concerning the creation of potions',NULL),('Smithing','A skill concerning the creation of items from metal',NULL);
/*!40000 ALTER TABLE `Skill` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-22 21:34:12
