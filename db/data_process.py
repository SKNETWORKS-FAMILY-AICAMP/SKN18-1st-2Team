import os
import pandas as pd
import re
import json

def get_project_root():
    # db/data_process.py 기준으로 상위 폴더(프로젝트 루트) 반환
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def do_process_data():
    ROOT_DIR = get_project_root()
    print("ROOT_DIR =", ROOT_DIR)

    json_path = os.path.join(ROOT_DIR, 'data', "ev_yearly_stats.json")
    csv_path = os.path.join(ROOT_DIR, 'data', "ev_yearly_stats.csv")
    output_path = os.path.join(ROOT_DIR, 'data', "ev_yearly_stats_long.csv")

    print("json_path =", json_path)
    print("csv_path =", csv_path)
    print("output_path =", output_path)

    if os.path.exists(json_path):
        print("JSON 파일을 사용합니다.")
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)
    elif os.path.exists(csv_path):
        print("CSV 파일을 사용합니다.")
        df = pd.read_csv(csv_path)
        data = df.to_dict(orient='records')
    else:
        raise FileNotFoundError("ev_yearly_stats.json 또는 ev_yearly_stats.csv 파일이 data 폴더에 존재해야 합니다.")

    rows = []
    for item in data:
        year = item.get('연월') or item.get('year') or item.get('Year')
        for region, value in item.items():
            if region in ['연월', 'year', 'Year', '계', 'Total']:
                continue
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

if __name__ == "__main__":
    do_process_data()
