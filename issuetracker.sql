DROP DATABASE IF EXISTS `issuetracker`;
CREATE DATABASE IF NOT EXISTS `issuetracker`;

USE `issuetracker`;

/*Table structure for table `user` */
CREATE TABLE `user` (
	`uid` int NOT NULL AUTO_INCREMENT,
	`email` varchar(40) DEFAULT NULL,
	`uname` varchar(40) DEFAULT NULL,
	`password` varchar(20) DEFAULT NULL,
	`disname` varchar(40) DEFAULT NULL,
	PRIMARY KEY (`uid`)
);

/*Data for the table `user` */
INSERT INTO `user` (`uid`, `email`, `uname`, `password`, `disname`) VALUES
(1060, 'sl2019@gmail.com', 'linda2019', '369852', 'Linda'),
(1088, 'hh370@foxmail.com', 'computerarch', '789456123', 'Haldun'),
(1666, 'yl2222@columbia.edu', 'lei2016', '888888', 'Yuan Lei'),
(1234, 'snox1999@gmail.com', 'snox2020', 's666666', 'GV_Snox'),
(7700, '125000@qq.com', 'xiaoemo', 'asdfgh', 'Zhi Zhou'),
(4790, 'jeff2018@gmail.com', 'jeff7878', '123455', 'Jeff Bezos');



/*Table structure for table `project` */
CREATE TABLE `project` (
	`pid` int NOT NULL AUTO_INCREMENT,
	`pname` varchar(40) DEFAULT NULL,
	`pdescription` varchar(500) DEFAULT NULL,
	`puid` int DEFAULT NULL,
	`ptime` datetime DEFAULT NULL,
	PRIMARY KEY (`pid`),
	CONSTRAINT `creprouser` FOREIGN KEY (`puid`) REFERENCES `user` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
);

/*Data for the table `project` */
INSERT INTO `project` (`pid`, `pname`, `pdescription`, `puid`, `ptime`) VALUES
(108, 'Amazon Kindle', 'It is a issue recorder of any sold Kindle on Amazon.', 1088, '2013-03-26 16:00:00'),
(186, 'Taobao Kindle', 'It is a issue recorder of any sold Kindle on Taobao.', 1060, '2013-07-19 13:30:25'),
(105, 'CSGO Server Maintainance', 'Project for the CSGO maintainance.', 1234, '2013-03-24 15:00:00'),
(135, 'Amazon Kindle', 'It is a sell recorder of any sold Kindle on Amazon.', 1060, '2013-03-26 16:00:00');


/*Table structure for table `lead` */
CREATE TABLE `lead` (
	`uid` int NOT NULL,
	`pid` int NOT NULL,
	PRIMARY KEY (`uid`, `pid`),
	CONSTRAINT `leaduser` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `leadpro` FOREIGN KEY (`pid`) REFERENCES `project` (`pid`) ON DELETE CASCADE ON UPDATE CASCADE
);

/*Data for the table `lead` */
INSERT INTO `lead` (`uid`, `pid`) VALUES
(1060, 108),
(1060, 186),
(1088, 108),
(1234, 105),
(1060, 135);


/*Table structure for table `status` */
CREATE TABLE `status` (
	`sid` int NOT NULL AUTO_INCREMENT,
	`sname` varchar(40) DEFAULT NULL,
	`sdescription` varchar(500) DEFAULT NULL,
	`spid` int NOT NULL,
	PRIMARY KEY (`sid`),
	CONSTRAINT `statuspro` FOREIGN KEY (`spid`) REFERENCES `project` (`pid`) ON DELETE CASCADE ON UPDATE CASCADE
);

/*Data for the table `status` */
INSERT INTO `status` (`sid`, `sname`, `sdescription`, `spid`) VALUES
(10801, 'OPEN', 'starting status', 108),
(10802, 'SOLVING', 'ternimating status', 108),
(10803, 'CLOSED', 'ternimating status', 108),
(10804, 'SOLVED', 'solved status', 108),
(18601, 'OPEN', 'starting status', 186),
(18602, 'SALES RETURN', 'return the sales with broken component', 186),
(18603, 'SALES EXCHANGE', 'exchange another new item', 186),
(18604, 'SALES FIX', 'fix the broken component of the item', 186),
(18605, 'CLOSED', 'ternimating status', 186),
(10501, 'OPEN', 'starting status', 105),
(10502, 'CLOSED', 'ternimating status', 105),
(13501, 'OPEN', 'starting status', 135),
(13502, 'CLOSED', 'ternimating status', 135);


/*Table structure for table `issue` */
CREATE TABLE `issue` (
	`iid` int NOT NULL AUTO_INCREMENT,
	`title` varchar(40) DEFAULT NULL,
	`idescription` varchar(500) DEFAULT NULL,
	`currentstatus` int DEFAULT NULL,
	`iuid` int DEFAULT NULL,
	`itime` datetime DEFAULT NULL,
	`ipid` int DEFAULT NULL,
	PRIMARY KEY (`iid`),
	CONSTRAINT `issuestatus` FOREIGN KEY (`currentstatus`) REFERENCES `status` (`sid`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `issuereporter` FOREIGN KEY (`iuid`) REFERENCES `user` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `issuepro` FOREIGN KEY (`ipid`) REFERENCES `project` (`pid`) ON DELETE CASCADE ON UPDATE CASCADE
);

/*Data for the table `issue` */
INSERT INTO `issue` (`iid`, `title`, `idescription`, `currentstatus`, `iuid`, `itime`, `ipid`) VALUES
(23, 'screen broken', 'The Kindle\'s screen is broken during the delivery.', 10803, 1666, '2013-04-26 16:00:00', 108),
(52, 'screen broken', 'The Kindle\'s screen is broken during the delivery.', 18601, 1666, '2013-04-28 16:00:00', 186),
(05, 'broken screen', 'The Kindle\'s screen is broken during the delivery.', 10801, 1666, '2013-05-26 16:00:00', 108),
(97, 'no batery', 'The Kindle\'s batery stops working.', 10801, 1666, '2013-06-26 16:00:00', 108),
(99, 'Server Crash', 'The server stops working.', 10502, 1234, '2013-07-26 16:00:00', 105);

/*Table structure for table `assign` */
CREATE TABLE `assign` (
	`uid` int NOT NULL,
	`auid` int NOT NULL,
	`iid` int NOT NULL,
	`atime` datetime DEFAULT NULL,
	PRIMARY KEY (`uid`, `auid`, `iid`),
	CONSTRAINT `assigner` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `assignee` FOREIGN KEY (`auid`) REFERENCES `user` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `assigniss` FOREIGN KEY (`iid`) REFERENCES `issue` (`iid`) ON DELETE CASCADE ON UPDATE CASCADE
);

/*Data for the table `assign` */
INSERT INTO `assign` (`uid`, `auid`, `iid`, `atime`) VALUES
(1060, 4790, 23, '2013-04-27 16:00:00'),
(1060, 1088, 23, '2013-04-27 16:00:00'),
(1060, 4790, 05, '2013-05-27 16:00:00'),
(1060, 4790, 97, '2013-06-27 16:00:00'),
(1060, 4790, 52, '2013-04-29 16:00:00'),
(1234, 7700, 99, '2013-04-29 16:00:00');


/*Table structure for table `statustrans` */
CREATE TABLE `statustrans` (
	`ssid` int NOT NULL,
	`tsid` int NOT NULL,
	PRIMARY KEY (`ssid`, `tsid`),
	CONSTRAINT `sourcestatus` FOREIGN KEY (`ssid`) REFERENCES `status` (`sid`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `tragetstatus` FOREIGN KEY (`tsid`) REFERENCES `status` (`sid`) ON DELETE CASCADE ON UPDATE CASCADE
);

/*Data for the table `statustrans` */
INSERT INTO `statustrans` (`ssid`, `tsid`) VALUES
(10801, 10802),
(10802, 10803),
(18601, 18602),
(18601, 18603),
(18601, 18604),
(18602, 18605),
(18603, 18605),
(18604, 18605),
(10501, 10502),
(13501, 13502),
(10802, 10804),
(10804, 10802);


/*Table structure for table `changestatus` */
CREATE TABLE `changestatus` (
	`uid` int NOT NULL,
	`iid` int NOT NULL,
	`ssid` int NOT NULL,
	`tsid` int NOT NULL,
	`supdatetime` datetime NOT NULL,
	PRIMARY KEY (`uid`, `iid`, `ssid`, `tsid`, `supdatetime`),
	CONSTRAINT `changestatususer` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `changestatuissue` FOREIGN KEY (`iid`) REFERENCES `issue` (`iid`) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `changesourcestatus` FOREIGN KEY (`ssid`, `tsid`) REFERENCES `statustrans` (`ssid`, `tsid`) ON DELETE CASCADE ON UPDATE CASCADE
);

/*Data for the table `changestatus` */
INSERT INTO `changestatus` (`uid`, `iid`, `ssid`, `tsid`, `supdatetime`) VALUES
(4790, 23, 10801, 10802, '2013-04-30 16:00:00'),
(4790, 23, 10802, 10803, '2013-05-05 16:00:00'),
(1234, 99, 10501, 10502, '2013-07-05 16:00:00'),
(4790, 23, 10802, 10804, '2013-05-01 16:00:00'),
(4790, 23, 10804, 10802, '2013-05-02 16:00:00'),
(4790, 23, 10802, 10804, '2013-05-03 16:00:00'),
(4790, 23, 10804, 10802, '2013-05-04 16:00:00');
