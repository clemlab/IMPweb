-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 16, 2018 at 05:38 AM
-- Server version: 10.2.15-MariaDB-10.2.15+maria~trusty-log
-- PHP Version: 5.5.9-1ubuntu4.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `impwebdb`
--
CREATE DATABASE IF NOT EXISTS `impwebdb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `impwebdb`;

-- --------------------------------------------------------

--
-- Table structure for table `batches`
--

DROP TABLE IF EXISTS `batches`;
CREATE TABLE IF NOT EXISTS `batches` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `job_name` varchar(100) NOT NULL,
  `is_public` tinyint(1) NOT NULL DEFAULT 1,
  `is_done` tinyint(1) NOT NULL DEFAULT 0,
  `submission_ip` varchar(50) DEFAULT NULL,
  `date_entered` datetime NOT NULL DEFAULT current_timestamp(),
  `date_started` datetime DEFAULT NULL,
  `date_completed` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `is_public` (`is_public`),
  KEY `is_done` (`is_done`),
  KEY `date_entered` (`date_entered`),
  KEY `date_completed` (`date_completed`),
  KEY `date_started` (`date_started`),
  FULLTEXT KEY `job_name` (`job_name`),
  FULLTEXT KEY `submission_ip` (`submission_ip`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=68 ;

--
-- Dumping data for table `batches`
--

INSERT INTO `batches` (`id`, `user_id`, `job_name`, `is_public`, `is_done`, `submission_ip`, `date_entered`, `date_started`, `date_completed`) VALUES
(1, 1, 'testflask', 1, 0, NULL, '2018-06-12 20:56:33', NULL, NULL),
(2, 1, 'testflask', 1, 0, NULL, '2018-06-12 20:58:14', NULL, NULL),
(3, 1, 'testflask', 1, 0, NULL, '2018-06-12 21:01:19', NULL, NULL),
(4, 1, 'testflask', 1, 0, NULL, '2018-06-12 21:03:41', NULL, NULL),
(16, 5, 'tesatsf', 1, 0, NULL, '2018-06-13 01:04:34', NULL, NULL),
(17, 5, 'tesatsf', 1, 0, NULL, '2018-06-13 01:05:54', NULL, NULL),
(18, 6, 'anothertestrun', 1, 0, NULL, '2018-06-13 01:10:14', NULL, NULL),
(19, 7, 'testsing1212', 1, 0, NULL, '2018-06-14 10:21:22', NULL, NULL),
(20, 7, 'testsing1212', 1, 0, NULL, '2018-06-14 10:22:42', NULL, NULL),
(21, 7, 'testsing1212', 1, 0, NULL, '2018-06-14 10:24:01', NULL, NULL),
(22, 7, 'testsing1212', 1, 0, NULL, '2018-06-14 10:26:09', NULL, NULL),
(23, 7, 'testsing1212', 1, 0, NULL, '2018-06-14 10:26:44', NULL, NULL),
(24, 7, 'testsing1212', 1, 0, NULL, '2018-06-14 10:27:15', NULL, NULL),
(25, 7, 'testsing1212', 1, 0, NULL, '2018-06-14 10:27:49', NULL, NULL),
(26, 7, 'testsing1212', 1, 0, NULL, '2018-06-14 10:28:37', NULL, NULL),
(27, 1, 'jsdaflksjdflkjlkjlk', 1, 0, NULL, '2018-06-14 17:48:14', NULL, NULL),
(28, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:42:16', NULL, NULL),
(29, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:43:00', NULL, NULL),
(30, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:43:16', NULL, NULL),
(31, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:43:55', NULL, NULL),
(32, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:44:04', NULL, NULL),
(33, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:44:41', NULL, NULL),
(34, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:44:55', NULL, NULL),
(35, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:45:37', NULL, NULL),
(36, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:46:07', NULL, NULL),
(37, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:46:31', NULL, NULL),
(38, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:49:38', NULL, NULL),
(39, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:53:00', NULL, NULL),
(40, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:53:51', NULL, NULL),
(41, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:56:56', NULL, NULL),
(42, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:57:30', NULL, NULL),
(43, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 19:57:43', NULL, NULL),
(44, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 20:12:59', NULL, NULL),
(45, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 20:14:03', NULL, NULL),
(46, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 20:27:31', NULL, NULL),
(47, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 20:27:47', NULL, NULL),
(48, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 20:30:28', NULL, NULL),
(49, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 20:55:02', NULL, NULL),
(50, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 20:55:40', NULL, NULL),
(51, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 20:56:51', NULL, NULL),
(52, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 20:59:18', NULL, NULL),
(53, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 21:11:28', NULL, NULL),
(54, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 21:19:35', NULL, NULL),
(55, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 21:23:25', NULL, NULL),
(56, 1, 'testingjobs', 1, 0, NULL, '2018-06-14 21:25:54', NULL, NULL),
(57, 1, 'testingjobs', 1, 0, NULL, '2018-06-15 01:03:00', NULL, NULL),
(58, 1, 'testingjobs', 1, 0, NULL, '2018-06-15 01:04:08', NULL, NULL),
(59, 1, 'testingjobs', 1, 0, NULL, '2018-06-15 01:23:13', NULL, NULL),
(60, 1, 'testingjobs', 1, 0, NULL, '2018-06-15 01:23:59', NULL, NULL),
(61, 1, 'testingjobs', 1, 0, NULL, '2018-06-15 01:26:29', NULL, NULL),
(62, 1, 'testingjobs', 1, 0, NULL, '2018-06-15 02:16:14', NULL, NULL),
(63, 1, 'Testjob1', 1, 0, NULL, '2018-06-15 02:59:23', NULL, NULL),
(64, 1, 'Testjob1', 1, 0, NULL, '2018-06-15 02:59:47', NULL, NULL),
(65, 1, 'secy_test', 1, 0, NULL, '2018-06-15 08:38:35', NULL, NULL),
(66, 1, 'secy_test', 1, 0, NULL, '2018-06-15 08:39:00', NULL, NULL),
(67, 1, 'secy_test', 1, 0, NULL, '2018-06-15 08:42:21', '2018-06-15 19:46:05', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `batch_scores`
--

DROP TABLE IF EXISTS `batch_scores`;
CREATE TABLE IF NOT EXISTS `batch_scores` (
  `batch_id` int(10) unsigned NOT NULL,
  `score_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`batch_id`,`score_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `batch_scores`
--

INSERT INTO `batch_scores` (`batch_id`, `score_id`) VALUES
(26, 10),
(27, 11),
(37, 12),
(38, 13),
(39, 14),
(40, 15),
(41, 16),
(42, 17),
(43, 18),
(43, 19),
(46, 15),
(46, 19),
(47, 15),
(47, 19),
(48, 15),
(48, 19),
(49, 15),
(49, 19),
(50, 15),
(50, 19),
(51, 15),
(51, 19),
(52, 15),
(52, 19),
(53, 15),
(53, 19),
(54, 15),
(54, 19),
(55, 15),
(55, 19),
(56, 15),
(56, 19),
(57, 15),
(57, 19),
(58, 15),
(58, 19),
(59, 15),
(59, 19),
(60, 15),
(60, 19),
(61, 15),
(61, 19),
(62, 15),
(62, 19),
(64, 20),
(66, 21),
(67, 22);

-- --------------------------------------------------------

--
-- Table structure for table `predictors`
--

DROP TABLE IF EXISTS `predictors`;
CREATE TABLE IF NOT EXISTS `predictors` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `protein_only` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `protein_only` (`protein_only`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `predictors`
--

INSERT INTO `predictors` (`id`, `name`, `protein_only`) VALUES
(1, 'improve_2018', 0);

-- --------------------------------------------------------

--
-- Table structure for table `scores`
--

DROP TABLE IF EXISTS `scores`;
CREATE TABLE IF NOT EXISTS `scores` (
  `sequence_id` char(32) NOT NULL,
  `predictor_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `score` double DEFAULT NULL,
  `data` longtext DEFAULT NULL,
  `error` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sequence_id`,`predictor_id`),
  UNIQUE KEY `id` (`id`),
  KEY `score` (`score`),
  KEY `seq_id` (`sequence_id`),
  KEY `predictor_id` (`predictor_id`),
  KEY `error` (`error`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=23 ;

--
-- Dumping data for table `scores`
--

INSERT INTO `scores` (`sequence_id`, `predictor_id`, `id`, `score`, `data`, `error`) VALUES
('249ed20dc6fd5e9ff0aaf9dd89457746', 1, 15, NULL, NULL, NULL),
('32fa127d31edfa6e4d33eb7dbc806061', 1, 12, NULL, NULL, NULL),
('49744084519029e8b79e36ea10ceb397', 1, 11, NULL, NULL, NULL),
('59906aeb00e4a0fa3976f62708d10963', 1, 22, -0.09213688, '{"title":"59906aeb00e4a0fa3976f6270","CAI":0.37,"Nc":48.29,"GC3s":0.525,"CpG":0.135,"tAI":0.3095505084,"CPS":9.7981205071,"CPSpL":0.0221176535,"deltaG":-514.75,"freqens":0.0,"40deltaG":-34.49,"40freqens":0.015046,"hotloops":4,"avgRONN":0.3619793531,"q25RONN":0.2921975951,"q75RONN":0.4093993094,"avgRONNloop":0.4043021466,"avgRONNextloop":0.3490285558,"avgRONNcytloop":0.4336082786,"avgRONNNterm":0.4893300959,"avgRONNCterm":0.5145315739,"avgRONNTM":0.3170975071,"RONNlongestloop":0.3695848458,"avgRONNTM1_2":0.4341311832,"numTMs":10,"avgTMlen":21.5,"membrCont":215,"membrContNorm":0.4853273138,"lenNterm":22,"lenNtermNorm":0.0496613995,"avgHydroGES":0.1038374718,"minhyd_19GES":-2.7052631579,"minhyd_41GES":-1.5317073171,"maxhyd_41GES":2.1170731707,"lenLoopAfterTM1":30,"loop1_avghydOCT":0.4623333333,"loop1_minhyd_OCT19":0.2473684211,"loop1_maxhyd_OCT19":0.6752631579,"HYD1stTM":-0.4554545455,"HYDallTMs":-0.435609283,"delG1stTM":0.588,"delGallTMs":-0.2986,"nterm_hydGES":0.95,"avgCU":21.4858783784,"avgCU_first40":24.92825,"avgCU_first20":23.771,"minCU_win5":21.516,"minCU_win10":20.169,"numPosCyt":32,"numPosNormCyt":0.214765,"numNegCyt":13,"numNegNormCyt":0.087248,"numPosExt":7,"numPosNormExt":0.088608,"numNegExt":6,"numNegNormExt":0.075949,"numPos_LongestCytLoop":9,"numNeg_LongestCytLoop":1,"numPos_LongestExtLoop":3,"numNeg_LongestExtLoop":3,"nterm_pos":5,"nterm_neg":2,"len1_2loop":30,"longestCytLoop":36,"longestCytLoopNorm":0.0812641084,"longestExtLoop":30,"longestExtLoopNorm":0.0677200903,"startCodon":1,"seqLen":443,"weight":48511.0903,"pI":9.8944702148,"aromatacityNorm":0.1151241535,"GPcount":2.5,"plus10valRNAss":0.311299,"zeroto38avgRNAss":0.4993924385,"zeroto38minRNAss":0.25274,"zeroto38q25RNAss":0.348991,"zeroto38q75RNAss":0.6382026,"zeroto38maxRNAss":0.72487773,"totalSDsites":82,"relareaSD":0.077046777,"codon16_36SD":1,"codon16_36relareaSD":0.0659955257,"codon40_60SD":1,"codon40_60relareaSD":0.0589485459,"minus5_plus2TM2SD":0,"minus5_plus2TM2relareaSD":0.0310003196,"tAI10Min":0.1190464091,"tAI10Max":0.5358436165,"tAI10q25":0.2777242694,"tAI10q75":0.3706206117,"GC":0.496996997,"GCdiffEC":-0.0222871621,"GC10min":0.3333333333,"GC10q25":0.4333333333,"GC10q75":0.5333333333,"GC10max":0.7333333333,"score":-0.09213688}', NULL),
('5decf4e4c2166dcc26e9b6423b076e20', 1, 20, NULL, NULL, NULL),
('64f76315b09acbcd820f4dfd405178d9', 1, 1, NULL, NULL, NULL),
('8374ba85d0c67c0241dbb7028360329c', 1, 19, NULL, NULL, NULL),
('9589c0052ff0dec7f06df12ea4c9e853', 1, 21, NULL, NULL, NULL),
('a3e8454be138626d298077496db4de42', 1, 4, NULL, NULL, NULL),
('ed9c408a9f34a40f9f42c3fab1eae19a', 1, 2, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `sequences`
--

DROP TABLE IF EXISTS `sequences`;
CREATE TABLE IF NOT EXISTS `sequences` (
  `id` char(32) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `seq` longtext NOT NULL,
  `protein_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `protein_id` (`protein_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sequences`
--

INSERT INTO `sequences` (`id`, `name`, `seq`, `protein_id`) VALUES
('249ed20dc6fd5e9ff0aaf9dd89457746', 'testseq2', 'sdajfklasdfjsaklfjsakldfjsda', NULL),
('32fa127d31edfa6e4d33eb7dbc806061', 'testseq2', '>testseq2\r\nsdajfklasdfjsaklfjsakldfjsda\r\n>testseq3\r\nasdfadsfasdfasfaf', NULL),
('49744084519029e8b79e36ea10ceb397', 'jsdaflksjdflkjlkjlk', 'testingsequence123', '64f76315b09acbcd820f4dfd405178d9'),
('59906aeb00e4a0fa3976f62708d10963', 'U00096.3:c3444097-3442766', 'ATGGCTAAACAACCGGGATTAGATTTTCAAAGTGCCAAAGGTGGCTTAGGCGAGCTGAAACGCAGACTGCTGTTTGTTATCGGTGCGCTGATTGTGTTCCGTATTGGCTCTTTTATTCCGATCCCTGGTATTGATGCCGCTGTACTTGCCAAACTGCTTGAGCAACAGCGAGGCACCATCATTGAGATGTTTAACATGTTCTCTGGTGGTGCTCTCAGCCGTGCTTCTATCTTTGCTCTGGGGATCATGCCGTATATTTCGGCGTCGATCATTATCCAGCTGCTGACGGTGGTTCACCCAACGTTGGCAGAAATTAAGAAAGAAGGGGAGTCTGGTCGTCGTAAGATCAGCCAGTACACCCGCTACGGTACTCTGGTGCTGGCAATATTCCAGTCGATCGGTATTGCTACCGGTCTGCCGAATATGCCTGGTATGCAAGGCCTGGTGATTAACCCGGGCTTTGCATTCTACTTCACCGCTGTTGTAAGTCTGGTCACAGGAACCATGTTCCTGATGTGGTTGGGCGAACAGATTACTGAACGAGGTATCGGCAACGGTATTTCAATCATTATCTTCGCCGGTATTGTCGCGGGACTCCCGCCAGCCATTGCCCATACTATCGAGCAAGCGCGTCAAGGCGACCTGCACTTCCTCGTGTTGCTGTTGGTTGCAGTATTAGTATTTGCAGTGACGTTCTTTGTTGTATTTGTTGAGCGTGGTCAACGCCGCATTGTGGTAAACTACGCGAAACGTCAGCAAGGTCGTCGTGTCTATGCTGCACAGAGCACACATTTACCGCTGAAAGTGAATATGGCGGGGGTAATCCCGGCAATCTTCGCTTCCAGTATTATTCTGTTCCCGGCGACCATCGCGTCATGGTTCGGGGGCGGTACTGGTTGGAACTGGCTGACAACAATTTCGCTGTATTTGCAGCCTGGGCAACCGCTTTATGTGTTACTCTATGCGTCTGCAATCATCTTCTTCTGTTTCTTCTACACGGCGTTGGTTTTCAACCCGCGTGAAACAGCAGATAACCTGAAGAAGTCCGGTGCATTTGTACCAGGAATTCGTCCGGGAGAGCAAACGGCGAAGTATATCGATAAAGTAATGACCCGCCTGACCCTGGTTGGTGCGCTGTATATTACCTTTATCTGCCTGATCCCGGAGTTCATGCGTGATGCAATGAAAGTACCGTTCTACTTCGGTGGGACCTCACTGCTTATCGTTGTTGTCGTGATTATGGACTTTATGGCTCAAGTGCAAACTCTGATGATGTCCAGTCAGTATGAGTCTGCATTGAAGAAGGCGAACCTGAAAGGCTACGGCCGATAA', NULL),
('5decf4e4c2166dcc26e9b6423b076e20', 'testfile', 'gaagagagagagagagagagagaagagagagagagagagagagataatatatatatataatatatatatatataat', NULL),
('64f76315b09acbcd820f4dfd405178d9', 'tesatsf', 'acacacacacacacacacacacaca', NULL),
('8374ba85d0c67c0241dbb7028360329c', 'testseq3', 'asdfadsfasdfasfaf', NULL),
('9589c0052ff0dec7f06df12ea4c9e853', 'sp|P0AGA2|SECY_ECOLI', 'MAKQPGLDFQSAKGGLGELKRRLLFVIGALIVFRIGSFIPIPGIDAAVLAKLLEQQRGTIIEMFNMFSGGALSRASIFALGIMPYISASIIIQLLTVVHPTLAEIKKEGESGRRKISQYTRYGTLVLAIFQSIGIATGLPNMPGMQGLVINPGFAFYFTAVVSLVTGTMFLMWLGEQITERG', NULL),
('a3e8454be138626d298077496db4de42', 'testsing1212', 'gagagagagagagagagagagagagagagagagagagagaga', '49744084519029e8b79e36ea10ceb397'),
('ed9c408a9f34a40f9f42c3fab1eae19a', 'anothertestrun', 'sdkfjhaskjdfhadskfjahdsfkjdahfads', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `sequence_translations`
--

DROP TABLE IF EXISTS `sequence_translations`;
CREATE TABLE IF NOT EXISTS `sequence_translations` (
  `prot_id` varchar(32) NOT NULL,
  `nuc_id` varchar(32) NOT NULL,
  PRIMARY KEY (`prot_id`,`nuc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `email` varchar(100) NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fullname` varchar(100) DEFAULT NULL,
  `institution` varchar(100) DEFAULT NULL,
  `public_jobs` tinyint(1) NOT NULL DEFAULT 1,
  `priority` varchar(10) NOT NULL DEFAULT 'med',
  `is_admin` tinyint(1) NOT NULL DEFAULT 0,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`email`),
  UNIQUE KEY `id` (`id`),
  KEY `institution` (`institution`),
  KEY `is_admin` (`is_admin`),
  KEY `is_active` (`is_active`),
  KEY `priority` (`priority`),
  KEY `keeppublic` (`public_jobs`),
  FULLTEXT KEY `fullname` (`fullname`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`email`, `id`, `fullname`, `institution`, `public_jobs`, `priority`, `is_admin`, `is_active`) VALUES
('oreogobbler+kindme@gmail.com', 7, NULL, NULL, 1, 'med', 0, 1),
('saladi@caltech.edu', 5, 'Shyam', 'Cal', 1, 'high', 0, 1),
('shyam+test@saladi.org', 6, NULL, NULL, 1, 'low', 0, 1),
('smsaladi@gmail.com', 1, 'Shyam Saladi', 'Caltech', 1, 'med', 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `user_batches`
--

DROP TABLE IF EXISTS `user_batches`;
CREATE TABLE IF NOT EXISTS `user_batches` (
  `user_id` int(10) unsigned NOT NULL,
  `batch_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`user_id`,`batch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
