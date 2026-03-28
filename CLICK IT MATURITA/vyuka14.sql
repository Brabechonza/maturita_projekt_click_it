-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 28, 2026 at 09:35 PM
-- Server version: 10.5.25-MariaDB
-- PHP Version: 8.2.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


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
-- Table structure for table `JB_games`
--

DROP TABLE IF EXISTS `JB_games`;
CREATE TABLE `JB_games` (
  `game_id` int(11) NOT NULL,
  `player_id` int(11) NOT NULL,
  `mode_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `player_at` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `JB_games`
--

INSERT INTO `JB_games` (`game_id`, `player_id`, `mode_id`, `score`, `player_at`) VALUES
(12, 11, 1, 50, '2026-02-12'),
(17, 14, 1, 49, '2026-02-18'),
(34, 28, 1, 41, '2026-03-26');

-- --------------------------------------------------------

--
-- Table structure for table `JB_modes`
--

DROP TABLE IF EXISTS `JB_modes`;
CREATE TABLE `JB_modes` (
  `mode_id` int(11) NOT NULL,
  `mode_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `JB_modes`
--

INSERT INTO `JB_modes` (`mode_id`, `mode_name`) VALUES
(1, '30s'),
(2, '2min');

-- --------------------------------------------------------

--
-- Table structure for table `JB_players`
--

DROP TABLE IF EXISTS `JB_players`;
CREATE TABLE `JB_players` (
  `player_id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `JB_players`
--

INSERT INTO `JB_players` (`player_id`, `username`) VALUES
(11, 'baf'),
(28, 'eliska'),
(14, 'honzaa');

-- --------------------------------------------------------

--
-- Table structure for table `JB_player_modes`
--

DROP TABLE IF EXISTS `JB_player_modes`;
CREATE TABLE `JB_player_modes` (
  `player_id` int(11) NOT NULL,
  `mode_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;

--
-- Dumping data for table `JB_player_modes`
--

INSERT INTO `JB_player_modes` (`player_id`, `mode_id`) VALUES
(11, 1),
(14, 1),
(28, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `JB_games`
--
ALTER TABLE `JB_games`
  ADD PRIMARY KEY (`game_id`),
  ADD KEY `player_id` (`player_id`),
  ADD KEY `mode_id` (`mode_id`);

--
-- Indexes for table `JB_modes`
--
ALTER TABLE `JB_modes`
  ADD PRIMARY KEY (`mode_id`);

--
-- Indexes for table `JB_players`
--
ALTER TABLE `JB_players`
  ADD PRIMARY KEY (`player_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `JB_player_modes`
--
ALTER TABLE `JB_player_modes`
  ADD PRIMARY KEY (`player_id`,`mode_id`),
  ADD KEY `fk_pm_mode` (`mode_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `JB_games`
--
ALTER TABLE `JB_games`
  MODIFY `game_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `JB_modes`
--
ALTER TABLE `JB_modes`
  MODIFY `mode_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `JB_players`
--
ALTER TABLE `JB_players`
  MODIFY `player_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `JB_games`
--
ALTER TABLE `JB_games`
  ADD CONSTRAINT `JB_games_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `JB_players` (`player_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `JB_games_ibfk_2` FOREIGN KEY (`mode_id`) REFERENCES `JB_modes` (`mode_id`) ON UPDATE CASCADE;

--
-- Constraints for table `JB_player_modes`
--
ALTER TABLE `JB_player_modes`
  ADD CONSTRAINT `fk_pm_mode` FOREIGN KEY (`mode_id`) REFERENCES `JB_modes` (`mode_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_pm_player` FOREIGN KEY (`player_id`) REFERENCES `JB_players` (`player_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
