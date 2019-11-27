-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Nov 26, 2019 alle 18:42
-- Versione del server: 10.1.40-MariaDB
-- Versione PHP: 7.3.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ota`
--
CREATE DATABASE IF NOT EXISTS `ota` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ota`;

-- --------------------------------------------------------

--
-- Struttura della tabella `accomodation`
--

CREATE TABLE `accomodation` (
  `IDhotel` int(11) NOT NULL,
  `NomeHotel` varchar(64) NOT NULL,
  `indirizzo` varchar(128) NOT NULL,
  `pazziPer` varchar(1000) DEFAULT NULL,
  `recensioni` varchar(3000) DEFAULT NULL,
  `motivi` varchar(500) DEFAULT NULL,
  `url` varchar(256) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `accomodationprice`
--

CREATE TABLE `accomodationprice` (
  `NomeHotel` varchar(200) NOT NULL,
  `PrezzoHotel` int(11) NOT NULL,
  `dataSoggiorno` date DEFAULT NULL,
  `dataRicerca` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `accomodationservice`
--

CREATE TABLE `accomodationservice` (
  `IDHotel` int(11) NOT NULL,
  `IDServizi` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `servizi`
--

CREATE TABLE `servizi` (
  `id` int(11) NOT NULL,
  `servizio` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `urlhotel`
--

CREATE TABLE `urlhotel` (
  `id` int(11) NOT NULL,
  `url` varchar(2048) NOT NULL,
  `data` date DEFAULT NULL,
  `citta` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `accomodation`
--
ALTER TABLE `accomodation`
  ADD PRIMARY KEY (`IDhotel`);

--
-- Indici per le tabelle `accomodationservice`
--
ALTER TABLE `accomodationservice`
  ADD PRIMARY KEY (`IDHotel`,`IDServizi`);

--
-- Indici per le tabelle `servizi`
--
ALTER TABLE `servizi`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `value_UNIQUE` (`servizio`);

--
-- Indici per le tabelle `urlhotel`
--
ALTER TABLE `urlhotel`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `accomodation`
--
ALTER TABLE `accomodation`
  MODIFY `IDhotel` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `servizi`
--
ALTER TABLE `servizi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `urlhotel`
--
ALTER TABLE `urlhotel`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
