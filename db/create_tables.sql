-- DB 생성/사용
CREATE DATABASE IF NOT EXISTS sknproject1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sknproject1;

-- 전기차 등록현황
CREATE TABLE IF NOT EXISTS ev_yearly_stats (
    year VARCHAR(10),
    seoul VARCHAR(50),
    busan VARCHAR(50),
    daegu VARCHAR(50),
    incheon VARCHAR(50),
    gwangju VARCHAR(50),
    daejeon VARCHAR(50),
    ulsan VARCHAR(50),
    sejong VARCHAR(50),
    gyeonggi VARCHAR(50),
    gangwon VARCHAR(50),
    chungbuk VARCHAR(50),
    chungnam VARCHAR(50),
    jeonbuk VARCHAR(50),
    jeonnam VARCHAR(50),
    gyeongbuk VARCHAR(50),
    gyeongnam VARCHAR(50),
    jeju VARCHAR(50),
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
