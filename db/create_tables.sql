-- DB 생성/사용
CREATE DATABASE IF NOT EXISTS sknproject1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sknproject1;

-- 전기차 등록현황
CREATE TABLE IF NOT EXISTS ev_yearly_stats (
 	year CHAR(4),
	region VARCHAR(20),
    total INT NOT NULL,
    PRIMARY KEY(year, region)
);

-- FAQ 테이블
CREATE TABLE IF NOT EXISTS kia_faq_data (
	faq_id INT AUTO_INCREMENT PRIMARY KEY, 
    category VARCHAR(100),
    question TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    image_urls TEXT,
    link_urls TEXT
);

-- 자동차 등록 통계 테이블
CREATE TABLE IF NOT EXISTS car_registration_stats (
    year VARCHAR(10),
    month VARCHAR(10),
    region VARCHAR(50),
    total VARCHAR(50),
    PRIMARY KEY (year, month, region)
);

-- 연료별 자동차 등록 대수
CREATE TABLE IF NOT EXISTS veh_fuel_stats(
    year varchar(10),
    sorting varchar(10),
    total int(30),
    gasoline int(30),
    diesel int(30),
    LPG int(30),
    hybrid int(30),
    elec int(30),
    hydrogen int(30),
    PRIMARY KEY(year)
);


-- 제조사별 전기차 시장 점유율율
CREATE TABLE IF NOT EXISTS ev_brand_stats(
    brand varchar(50),
    year int(20),
    year_rate varchar(20),
    PRIMARY KEY(brand, year)
);

CREATE TABLE IF NOT EXISTS ev_region_stats(
    region varchar(20),
    year int(20),
    elec int(20),
    hydrogen int(20),
    hybrid int(20),
    eco int(20),
    PRIMARY KEY(region, year)
);