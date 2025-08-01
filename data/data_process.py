import os
import pandas as pd
import re
import json

# data 폴더 내 파일 경로 설정
data_dir = os.path.dirname(os.path.abspath(__file__))

# 파일명 설정
json_path = os.path.join(data_dir, "ev_yearly_stats.json")
csv_path = os.path.join(data_dir, "ev_yearly_stats.csv")
output_path = os.path.join(data_dir, "ev_yearly_stats_long.csv")

# 파일 자동 감지 (json 우선, 없으면 csv)
if os.path.exists(json_path):
    print("JSON 파일을 사용합니다.")
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    file_used = json_path
elif os.path.exists(csv_path):
    print("CSV 파일을 사용합니다.")
    df = pd.read_csv(csv_path)
    data = df.to_dict(orient='records')
    file_used = csv_path
else:
    raise FileNotFoundError("ev_yearly_stats.json 또는 ev_yearly_stats.csv 파일이 data 폴더에 존재해야 합니다.")

# 변환 (ratio 없이)
rows = []
for item in data:
    year = item.get('연월') or item.get('year') or item.get('Year')
    for region, value in item.items():
        if region in ['연월', 'year', 'Year', '계', 'Total']:
            continue
        # "숫자 (비율)" 패턴에서 숫자만 추출
        match = re.match(r'([\d,]+)', str(value))
        if match:
            total = int(match.group(1).replace(',', ''))
            rows.append({
                'year': int(year),
                'region': region,
                'total': total
            })

df_long = pd.DataFrame(rows)

print(df_long.head())
df_long.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"변환 완료! 저장 위치: {output_path}")

# 기존 파일 삭제
files_to_remove = []
if os.path.exists(json_path):
    files_to_remove.append(json_path)
if os.path.exists(csv_path):
    files_to_remove.append(csv_path)

for file_path in files_to_remove:
    try:
        os.remove(file_path)
        print(f"삭제 완료: {file_path}")
    except Exception as e:
        print(f"삭제 실패: {file_path}, 사유: {e}")
