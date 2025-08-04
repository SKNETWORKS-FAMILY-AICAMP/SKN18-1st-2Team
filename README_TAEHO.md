# 1. requirements.txt 확인하고 설치
# 2. data/crawl_car_data.py 실행하여 크롤링
# -> data/car_excels 폴더에 엑셀파일 생성 확인
# 3. db/create_tables.sql [Dbeaber에서] 실행하여 엑셀파일 합쳐서 CSV파일로 변환
# -> car_registration_stats.csv 생성 확인
# 4. db/insert_car_csv_data.py 실행하여 DB에 삽입해주기. 