-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: MyLeader
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Accounts`
--

DROP TABLE IF EXISTS `Accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Accounts` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Login` varchar(60) COLLATE utf8_polish_ci DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Accounts`
--

LOCK TABLES `Accounts` WRITE;
/*!40000 ALTER TABLE `Accounts` DISABLE KEYS */;
/*!40000 ALTER TABLE `Accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Functions`
--

DROP TABLE IF EXISTS `Functions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Functions` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `FunctionName` varchar(100) COLLATE utf8_polish_ci NOT NULL,
  `Description` text COLLATE utf8_polish_ci NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Functions`
--

LOCK TABLES `Functions` WRITE;
/*!40000 ALTER TABLE `Functions` DISABLE KEYS */;
INSERT INTO `Functions` VALUES (5,'Administrator','Can create groups, tasks, users and manage them.'),(10,'User','Standard user who can receive and do tasks.');
/*!40000 ALTER TABLE `Functions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Groups`
--

DROP TABLE IF EXISTS `Groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Groups` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `GroupName` varchar(400) COLLATE utf8_polish_ci NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Groups`
--

LOCK TABLES `Groups` WRITE;
/*!40000 ALTER TABLE `Groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `Groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Membership`
--

DROP TABLE IF EXISTS `Membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Membership` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `GroupID` int(10) unsigned NOT NULL,
  `AccountID` int(10) unsigned NOT NULL,
  `FunctionID` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Membership_Accounts_FK` (`AccountID`),
  KEY `Membership_Groups_FK` (`GroupID`),
  KEY `Membership_Functions_FK` (`FunctionID`),
  CONSTRAINT `Membership_Accounts_FK` FOREIGN KEY (`AccountID`) REFERENCES `Accounts` (`ID`),
  CONSTRAINT `Membership_Functions_FK` FOREIGN KEY (`FunctionID`) REFERENCES `Functions` (`ID`),
  CONSTRAINT `Membership_Groups_FK` FOREIGN KEY (`GroupID`) REFERENCES `Groups` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Membership`
--

LOCK TABLES `Membership` WRITE;
/*!40000 ALTER TABLE `Membership` DISABLE KEYS */;
/*!40000 ALTER TABLE `Membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SubTasks`
--

DROP TABLE IF EXISTS `SubTasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SubTasks` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `TaskID` int(10) unsigned NOT NULL,
  `Description` text COLLATE utf8_polish_ci NOT NULL,
  `AccountID` int(10) unsigned NOT NULL,
  `StateID` int(10) unsigned NOT NULL,
  `Localisation` varchar(100) COLLATE utf8_polish_ci NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `SubTasks_Accounts_FK` (`AccountID`),
  KEY `SubTasks_TaskState_FK` (`StateID`),
  KEY `SubTasks_Tasks_FK` (`TaskID`),
  CONSTRAINT `SubTasks_Accounts_FK` FOREIGN KEY (`AccountID`) REFERENCES `Accounts` (`ID`),
  CONSTRAINT `SubTasks_TaskState_FK` FOREIGN KEY (`StateID`) REFERENCES `TaskStates` (`ID`),
  CONSTRAINT `SubTasks_Tasks_FK` FOREIGN KEY (`TaskID`) REFERENCES `Tasks` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SubTasks`
--

LOCK TABLES `SubTasks` WRITE;
/*!40000 ALTER TABLE `SubTasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `SubTasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TaskStates`
--

DROP TABLE IF EXISTS `TaskStates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TaskStates` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `TaskState` varchar(100) COLLATE utf8_polish_ci NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TaskStates`
--

LOCK TABLES `TaskStates` WRITE;
/*!40000 ALTER TABLE `TaskStates` DISABLE KEYS */;
INSERT INTO `TaskStates` VALUES (10,'Stworzone'),(20,'Przydzielone'),(30,'W trakcie'),(40,'Zakończone');
/*!40000 ALTER TABLE `TaskStates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Tasks`
--

DROP TABLE IF EXISTS `Tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tasks` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `GroupID` int(10) unsigned NOT NULL,
  `Title` varchar(200) COLLATE utf8_polish_ci NOT NULL,
  `Description` text COLLATE utf8_polish_ci NOT NULL,
  `StateID` int(10) unsigned NOT NULL,
  `Localisation` varchar(100) COLLATE utf8_polish_ci NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Tasks_Groups_FK` (`GroupID`),
  KEY `Tasks_TaskState_FK` (`StateID`),
  CONSTRAINT `Tasks_Groups_FK` FOREIGN KEY (`GroupID`) REFERENCES `Groups` (`ID`),
  CONSTRAINT `Tasks_TaskState_FK` FOREIGN KEY (`StateID`) REFERENCES `TaskStates` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tasks`
--

LOCK TABLES `Tasks` WRITE;
/*!40000 ALTER TABLE `Tasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `Tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `AccountID` int(10) unsigned NOT NULL,
  `FirstName` varchar(50) CHARACTER SET utf8 NOT NULL,
  `LastName` varchar(50) CHARACTER SET utf8 NOT NULL,
  `Email` varchar(50) CHARACTER SET utf8 NOT NULL,
  `Password` varchar(256) CHARACTER SET utf8 NOT NULL,
  `SaltID` int(10) unsigned NOT NULL,
  `Activated` tinyint(1) DEFAULT '0',
  `Reset` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ID`),
  KEY `Users_Accounts_FK` (`AccountID`),
  CONSTRAINT `Users_Accounts_FK` FOREIGN KEY (`AccountID`) REFERENCES `Accounts` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-27  0:00:22
