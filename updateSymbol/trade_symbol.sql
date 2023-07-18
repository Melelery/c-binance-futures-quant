/******************************************/
/*   DatabaseName = real   */
/*   TableName = trade_symbol   */
/******************************************/
CREATE TABLE `trade_symbol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbol` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `coin` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `quote` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `onboardDate` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `index` int DEFAULT NULL,
  `defaultShow` int DEFAULT NULL,
  `onboardTs` int DEFAULT NULL,
  `linkSymbolArr` json DEFAULT NULL,
  `quoteVolume` double(30,10) DEFAULT '0.0000000000',
  `quoteVolumeRank` int DEFAULT NULL,
  `linkPrivateIP` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `machineRunTs` bigint DEFAULT '0',
  `machineRunTime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `symbol` (`symbol`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=179 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC
;
