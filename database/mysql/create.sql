-- 数据库
CREATE DATABASE IF NOT EXISTS `gunsupgame` DEFAULT CHARACTER SET utf8;

USE `gunsupgame`;

-- 联盟表 alliance
CREATE TABLE IF NOT EXISTS `alliance` (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `url_id` VARCHAR(32) NOT NULL,
    `name` VARCHAR(128) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`url_id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

-- 盟战赛季表 season
CREATE TABLE IF NOT EXISTS `season` (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `serial_id` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`serial_id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

-- 联盟赛季得分表 alliance_season_point
CREATE TABLE IF NOT EXISTS `alliance_season_point` (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `alliance_id` bigint(20) NOT NULL,
    `season_id` bigint(20) NOT NULL,
    `crawl_time` TIMESTAMP NOT NULL,
    `victory_point` int NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`alliance_id`) REFERENCES `alliance`(`id`),
    FOREIGN KEY (`season_id`) REFERENCES `season`(`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
