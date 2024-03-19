--
-- Database: `Weight`
--

CREATE DATABASE IF NOT EXISTS `weight`;

-- --------------------------------------------------------

--
-- Table structure for table `containers-registered`
--

USE weight;


CREATE TABLE IF NOT EXISTS `containers_registered` (
  `container_id` varchar(15) NOT NULL,
  `weight` int(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`container_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `datetime` datetime DEFAULT NULL,
  `direction` varchar(10) DEFAULT NULL,
  `truck` varchar(50) DEFAULT NULL,
  `containers` varchar(10000) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `truckTara` int(12) DEFAULT NULL,
  `neto` int(12) DEFAULT NULL,
  `produce` varchar(50) DEFAULT NULL,
  `session_id` int(12) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

show tables;

INSERT INTO transactions (datetime, direction, truck, bruto, truckTara, neto, produce, session_id) 
VALUES ('2024-03-20 10:00:00', 'IN', 'Truck1', 20000, 10000, 10000, 'Apples', 12345);

INSERT INTO transactions (datetime, direction, truck, containers, bruto, truckTara, neto, produce, session_id) 
VALUES ('2024-03-21 08:00:00', 'IN', 'Truck2', 'container1,container2,container3', 30000, 10000, 20000, 'Oranges', 12346);

INSERT INTO transactions (datetime, direction, truck, containers, bruto, truckTara, neto, produce, session_id) 
VALUES ('2024-03-22 09:00:00', 'IN', 'Truck3', 'container1,container2', 25000, 10000, 15000, 'Bananas', 12347);

INSERT INTO transactions (datetime, direction, truck, containers, bruto, truckTara, neto, session_id) 
VALUES ('2024-03-23 10:30:00', 'OUT', 'Truck4', 'container1,container2,container3', 35000, 10000, 25000, 12348);

INSERT INTO transactions (datetime, direction, truck, containers, bruto, truckTara, neto, produce, session_id) 
VALUES ('2024-03-24 11:00:00', 'OUT', 'Truck5', 'container1', 18000, 10000, 8000, 'Pineapples', 12349);

describe containers_registered;
describe transactions;



--
-- Dumping data for table `test`
--

-- INSERT INTO `test` (`id`, `aa`) VALUES
-- (1, 'aaaa'),
