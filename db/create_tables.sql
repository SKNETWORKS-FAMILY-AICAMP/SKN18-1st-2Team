-- DB 생성/사용
CREATE DATABASE IF NOT EXISTS sknproject1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sknproject1;

-- 전기차 등록현황
CREATE TABLE IF NOT EXISTS ev_yearly_stats (
    year VARCHAR(10),
    region VARCHAR(50),
    total VARCHAR(50)
);

-- FAQ 테이블
CREATE TABLE IF NOT EXISTS kia_faq_data (
    category VARCHAR(100),
    question TEXT,
    answer_text TEXT,
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