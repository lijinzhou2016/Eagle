/*
 Navicat Premium Data Transfer

 Source Server         : android
 Source Server Type    : SQLite
 Source Server Version : 3008008
 Source Database       : main

 Target Server Type    : SQLite
 Target Server Version : 3008008
 File Encoding         : utf-8

 Date: 05/12/2017 13:57:38 PM
*/

PRAGMA foreign_keys = false;

-- ----------------------------
--  Table structure for _devices_old_20170512
-- ----------------------------
DROP TABLE IF EXISTS "_devices_old_20170512";
CREATE TABLE "_devices_old_20170512" (
	 "id" int(8,0) NOT NULL,
	 "serial" TEXT(16,0) NOT NULL,
	 "runtime" float(8,2),
	PRIMARY KEY("id")
);

-- ----------------------------
--  Table structure for _devices_old_20170512_1
-- ----------------------------
DROP TABLE IF EXISTS "_devices_old_20170512_1";
CREATE TABLE "_devices_old_20170512_1" (
	 "id" int(8,0) NOT NULL,
	 "serial" TEXT(16,0) NOT NULL,
	 "runtime" float(8,2) NOT NULL,
	 "total_case" int(8,0) NOT NULL,
	 "fail_case" int(8,0) NOT NULL,
	 "success_case" int,
	PRIMARY KEY("id")
);

-- ----------------------------
--  Table structure for _devices_old_20170512_2
-- ----------------------------
DROP TABLE IF EXISTS "_devices_old_20170512_2";
CREATE TABLE "_devices_old_20170512_2" (
	 "id" int(8,0) NOT NULL,
	 "serial" TEXT(16,0) NOT NULL,
	 "runtime" float(8,2) NOT NULL,
	 "total_case" int(8,0) NOT NULL,
	 "fail_case" int(8,0) NOT NULL,
	 "pass_case" int,
	 "finished_case" TEXT,
	 "crash" TEXT,
	 "reboot" TEXT,
	 "anr" TEXT,
	 "tombstone" TEXT,
	PRIMARY KEY("id")
);

-- ----------------------------
--  Table structure for _devices_old_20170512_3
-- ----------------------------
DROP TABLE IF EXISTS "_devices_old_20170512_3";
CREATE TABLE "_devices_old_20170512_3" (
	 "id" int(8,0) NOT NULL,
	 "serial" TEXT(16,0) NOT NULL,
	 "runtime" float(8,2) NOT NULL,
	 "total_case" int(8,0) NOT NULL,
	 "fail_case" int(8,0) NOT NULL,
	 "pass_case" int NOT NULL,
	 "finished_case" TEXT NOT NULL DEFAULT 0,
	 "crash" TEXT NOT NULL DEFAULT 0,
	 "reboot" TEXT NOT NULL DEFAULT 0,
	 "anr" TEXT NOT NULL DEFAULT 0,
	 "tombstone" TEXT NOT NULL DEFAULT 0,
	PRIMARY KEY("id")
);

-- ----------------------------
--  Table structure for devices
-- ----------------------------
DROP TABLE IF EXISTS "devices";
CREATE TABLE "devices" (
	 "id" int(8,0) NOT NULL,
	 "serial" TEXT(16,0) NOT NULL,
	 "runtime" float(8,2) NOT NULL DEFAULT 0,
	 "total_case" int(8,0) NOT NULL,
	 "fail_case" int(8,0) NOT NULL,
	 "pass_case" int NOT NULL,
	 "finished_case" TEXT NOT NULL DEFAULT 0,
	 "crash" TEXT NOT NULL DEFAULT 0,
	 "reboot" TEXT NOT NULL DEFAULT 0,
	 "anr" TEXT NOT NULL DEFAULT 0,
	 "tombstone" TEXT NOT NULL DEFAULT 0,
	PRIMARY KEY("id")
);

-- ----------------------------
--  Table structure for serial1
-- ----------------------------
DROP TABLE IF EXISTS "serial1";
CREATE TABLE "serial1" (
	 "id" int(32,0) NOT NULL,
	PRIMARY KEY("id")
);

PRAGMA foreign_keys = true;
