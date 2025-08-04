# 1. requirements.txt 확인하고 설치

# 2. .\data\crawl_car_data.py 실행하여 크롤링

# -> data/car_excels 폴더에 엑셀파일 생성 확인

# 3. .\data\excel_to_csv_converter.py 실행하여 csv파일로 변환

# -> car_registration_stats.csv 생성 확인

# 4. [Dbeaber에서] db/create_tables.sql 한줄씩 실행하기

# -> [Dbeaber에서] 새 테이블 (car_registration_stats) 생성된거 확인.

# 5. .\db\insert_car_csv_data.py 실행하여 DB에 삽입해주기.

# -> [Dbeaber에서] car_registration_stats.csv 테이블에 데이터 삽입된거 확인

# 6. # 마지막에 웹앱 실행 streamlit run main.py