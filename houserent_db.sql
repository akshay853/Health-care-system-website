-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Aug 01, 2021 at 12:00 PM
-- Server version: 10.4.20-MariaDB
-- PHP Version: 8.0.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `houserent_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `paying_guest_details` varchar(100) CHARACTER SET utf8 NOT NULL,
  `rent_house_details` varchar(100) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`paying_guest_details`, `rent_house_details`) VALUES
('14', 'paying guest'),
('22', 'rent house'),
('15', 'rent house'),
('5', 'paying guest'),
('11', 'paying guest');

-- --------------------------------------------------------

--
-- Table structure for table `complaint`
--

CREATE TABLE `complaint` (
  `name` varchar(50) CHARACTER SET utf8 NOT NULL,
  `description` varchar(100) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `complaint`
--

INSERT INTO `complaint` (`name`, `description`) VALUES
('akshay ', 'invalid coupon');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `id` int(11) NOT NULL,
  `username` varchar(50) CHARACTER SET utf8 NOT NULL,
  `password` varchar(50) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `owner_reg`
--

CREATE TABLE `owner_reg` (
  `o_id` int(20) NOT NULL,
  `name` varchar(50) CHARACTER SET utf8 NOT NULL,
  `address` varchar(100) CHARACTER SET utf8 NOT NULL,
  `phone_no` int(20) NOT NULL,
  `password` varchar(50) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `owner_reg`
--

INSERT INTO `owner_reg` (`o_id`, `name`, `address`, `phone_no`, `password`) VALUES
(123, 'ow', 'qwertyui', 1234567890, 'ow'),
(123, 'ow', 'qwertyui', 1234567890, 'ow');

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `payment_id` int(50) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 NOT NULL,
  `amount` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`payment_id`, `name`, `amount`) VALUES
(1234, 'akshay', 4573.9);

-- --------------------------------------------------------

--
-- Table structure for table `property`
--

CREATE TABLE `property` (
  `ownerd` varchar(100) CHARACTER SET utf8 NOT NULL,
  `Loc` varchar(100) CHARACTER SET utf8 NOT NULL,
  `plot` int(20) NOT NULL,
  `prodes` varchar(100) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `property`
--

INSERT INTO `property` (`ownerd`, `Loc`, `plot`, `prodes`) VALUES
('t1r1', 'fgwwgfwgfwg', 11111, 'vsbvdtsfvbsd'),
('123', 'wertyui', 1234567, 'qwertygvvbh'),
('123', 'wertyui', 1234567, 'qwertygvvbh');

-- --------------------------------------------------------

--
-- Table structure for table `user_reg`
--

CREATE TABLE `user_reg` (
  `user_id` int(20) NOT NULL,
  `name` varchar(50) CHARACTER SET utf8 NOT NULL,
  `address` varchar(100) CHARACTER SET utf8 NOT NULL,
  `phone_no` int(20) NOT NULL,
  `password` varchar(50) CHARACTER SET utf8 NOT NULL,
  `options` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_reg`
--

INSERT INTO `user_reg` (`user_id`, `name`, `address`, `phone_no`, `password`, `options`) VALUES
(123456, 'ak', 'aksh', 1234567890, '123', 'user'),
(123, 'admin', 'aksh', 1234567890, 'admin', 'admin'),
(111, 'owner', 'owner house', 1234567890, 'owner', 'owner');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
