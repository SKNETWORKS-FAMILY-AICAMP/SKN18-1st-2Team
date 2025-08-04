import pandas as pd
import os
import re
from glob import glob

def clean_numeric_value(value):
    """숫자 값 정리 함수"""
    if pd.isna(value) or value == '' or value == '-':
        return 0
    try:
        if isinstance(value, str):
            value = value.replace(',', '').replace(' ', '')
        return int(float(value))
    except:
        return 0

def extract_year_month(filename):
    """파일명에서 년월 추출"""
    match = re.search(r'(\d{4})년_(\d{1,2})월', filename)
    if match:
        year = match.group(1)
        month = match.group(2).zfill(2)
        return year, month
    return None, None

def process_excel_to_csv():
    """모든 엑셀 파일을 CSV로 변환"""
    # 엑셀 파일 경로
    excel_dir = 'car_excels'
    excel_files = glob(os.path.join(excel_dir, '*.xlsx'))
    excel_files.sort()
    
    all_data = []
    
    print(f"총 {len(excel_files)}개 엑셀 파일 처리 시작...")
    
    for file_path in excel_files:
        filename = os.path.basename(file_path)
        year, month = extract_year_month(filename)
        
        if not year or not month:
            print(f"파일명에서 년월 추출 실패: {filename}")
            continue
            
        print(f"처리 중: {filename} -> {year}년 {month}월")
        
        try:
            # 01.통계표 시트 읽기
            df = pd.read_excel(file_path, sheet_name='01.통계표', header=None)
            
            # 시도명 목록
            regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', 
                      '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
            
            # 데이터 시작 행 찾기 (시도별이 있는 행 다음부터)
            data_start_row = 5  # 앞서 확인한 결과로는 5행부터 시작
            
            for i in range(data_start_row, len(df)):
                row = df.iloc[i]
                region_name = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ''
                
                if region_name in regions:
                    try:
                        # 총합계 데이터 추출 (21번째 열)
                        grand_total = clean_numeric_value(row.iloc[21])
                        
                        all_data.append({
                            'year': year,
                            'month': month,
                            'region': region_name,
                            'total': grand_total
                        })
                    except Exception as e:
                        print(f"  행 파싱 오류 {region_name}: {e}")
                        continue
                        
            print(f"  처리 완료")
            
        except Exception as e:
            print(f"파일 처리 오류 {filename}: {e}")
            continue
    
    # CSV 파일로 저장
    if all_data:
        df_result = pd.DataFrame(all_data)
        output_file = 'car_registration_stats.csv'
        df_result.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n변환 완료!")
        print(f"저장된 파일: {output_file}")
        print(f"총 레코드 수: {len(all_data)}")
        print(f"기간: {df_result['year'].min()}년 {df_result['month'].min()}월 ~ {df_result['year'].max()}년 {df_result['month'].max()}월")
        print(f"지역 수: {df_result['region'].nunique()}개")
        
        # 샘플 데이터 출력
        print(f"\n샘플 데이터:")
        print(df_result.head(10))
    else:
        print("변환할 데이터가 없습니다.")

if __name__ == "__main__":
    process_excel_to_csv()