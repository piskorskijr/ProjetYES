-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Client :  localhost:3306
-- Généré le :  Lun 12 Octobre 2020 à 11:18
-- Version du serveur :  10.3.23-MariaDB-0+deb10u1
-- Version de PHP :  7.3.19-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `TestProjetYES`
--

-- --------------------------------------------------------

--
-- Structure de la table `comptage`
--

CREATE TABLE `comptage` (
  `cycliste` int(255) NOT NULL,
  `COULEUR_AIR` varchar(50) DEFAULT NULL,
  `valeur_air` varchar(40) DEFAULT NULL,
  `qualif_air` varchar(40) DEFAULT NULL,
  `id` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Contenu de la table `comptage`
--

INSERT INTO `comptage` (`cycliste`, `COULEUR_AIR`, `valeur_air`, `qualif_air`, `id`) VALUES
(0, '#99E600', '3', 'Bon', 1);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
