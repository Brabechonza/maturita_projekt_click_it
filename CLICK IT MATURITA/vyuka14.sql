-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 18, 2026 at 12:59 PM
-- Server version: 10.5.25-MariaDB
-- PHP Version: 8.2.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vyuka14`
--
CREATE DATABASE IF NOT EXISTS `vyuka14` DEFAULT CHARACTER SET utf8 COLLATE utf8_czech_ci;
USE `vyuka14`;

-- --------------------------------------------------------

--
-- Table structure for table `games`
--

DROP TABLE IF EXISTS `games`;
CREATE TABLE IF NOT EXISTS `games` (
  `game_id` int(11) NOT NULL AUTO_INCREMENT,
  `player_id` int(11) NOT NULL,
  `mode_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `player_at` date NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`game_id`),
  KEY `player_id` (`player_id`),
  KEY `mode_id` (`mode_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `games`
--

INSERT INTO `games` (`game_id`, `player_id`, `mode_id`, `score`, `player_at`) VALUES
(6, 6, 1, 41, '2026-02-03'),
(9, 8, 1, 48, '2026-02-10'),
(10, 9, 1, 51, '2026-02-10'),
(12, 11, 1, 50, '2026-02-12');

-- --------------------------------------------------------

--
-- Table structure for table `modes`
--

DROP TABLE IF EXISTS `modes`;
CREATE TABLE IF NOT EXISTS `modes` (
  `mode_id` int(11) NOT NULL AUTO_INCREMENT,
  `mode_name` varchar(20) NOT NULL,
  PRIMARY KEY (`mode_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `modes`
--

INSERT INTO `modes` (`mode_id`, `mode_name`) VALUES
(1, '30s'),
(2, '2min');

-- --------------------------------------------------------

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
CREATE TABLE IF NOT EXISTS `players` (
  `player_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  PRIMARY KEY (`player_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `players`
--

INSERT INTO `players` (`player_id`, `username`) VALUES
(8, 'ahoj'),
(11, 'cauy'),
(6, 'cus bus autobus'),
(9, 'honzaa');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `games`
--
ALTER TABLE `games`
  ADD CONSTRAINT `games_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `games_ibfk_2` FOREIGN KEY (`mode_id`) REFERENCES `modes` (`mode_id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
