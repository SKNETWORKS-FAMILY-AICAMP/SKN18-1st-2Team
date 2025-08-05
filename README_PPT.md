# 단위프로젝트 2팀 PT
## 전국 자동차 등록 현황 및 기업 FAQ 조회 시스템 

## Team Information

Team Name : sknproject18기 2조

|  이름  	| 역 할 	| 세부 역할 	|     Github    	|
|:------:	|:-----:	|:---------:	|:------------- 	|
| 정동석 	| 팀장  	| 등록 현황 	| @dsj-1004     	|
| 황혜진 	| 팀원  	| FAQ 	| @HJincode     	|
| 김준규 	| 팀원  	| FAQ 	| @JungyuOO     	|
| 양진아 	| 팀원  	| 등록 현황 	| @JINA1003 	|
| 이태호 	| 팀원  	| 등록 현황 	| @william7333     	|

Stacks 📚
Environment
!Visual Studio Code
!Git
!Github

Development
!Python 
!MySQL
!Streamlit
!Docker


Communication
!Discord 


### 요구사항 
- 데이터 수집 및 통합
- 데이터베이스 설계 및 구축
- 자동차 등록 현황 조회 시스템
- FAQ 검색 및 질문 응답 시스템
- 시각화 및 사용자 UI

### 수집 데이터
- 전기차 등록 현황 사이트 : https://chargeinfo.ksga.org/front/statistics/evCar/
- 국토교통부 250122(석간)자동차누적등록대수_26_298천대(자동차운영보험과).pdf
- 자동차등록현황보고 : https://stat.molit.go.kr/portal/cate/statMetaView.do?hRsId=58
- Kia FAQ 사이트: https://www.kia.com/kr/customer-service/center/faq

### ERD
<img width="656" height="438" alt="스크린샷 2025-08-05 10 30 04" src="https://github.com/user-attachments/assets/e5a75aa7-42fc-4018-b0d0-b358801ddbd0" />

### 화면 구성
- <img width="216" height="192" alt="image" src="https://github.com/user-attachments/assets/98a68263-74d4-41eb-8667-4e89fc6f2853" />


### 인사이트
1. 전기차 등록 비율의 상승
전기차 등록 데이터 분석을 통해 최근 5년 사이 꾸준한 성장세가 확인됨.

2. 지역별 자동차 등록 현황 차이
전국 단위 자동차 등록 현황 데이터를 비교한 결과:
경기도, 서울, 부산이 등록대수 상위 지역.
반면 세종, 제주, 강원 등은 전체 등록대수는 적지만, 전기차 비율이 상대적으로 높음.

3.연도별 등록 추세 분석
연도별 자동차 전체 등록대수와 전기차 등록대수의 추세 비교를 통해:
전체 자동차 등록 증가율은 둔화, 반면 전기차는 연평균 두 자릿수 성장률 유지.


### 오류 목록
- 이슈 목록 : https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN18-1st-2Team/issues?q=is%3Aissue%20state%3Aclosed

### 각자 느낀점
- 정동석 : 
- 김준규 : Streamlit을 활용해 페이지를 구현하면서 예상보다 제약이 많아 어려움을 느꼈습니다. 또한, 크롤링으로 수집한 데이터를 데이터베이스에 저장하고 이를 화면에 출력하는 과정을 오랜만에 진행해보니 흥미로웠습니다. 직접 여러 페이지에서 크롤링을 해보면서, 페이지마다 구조와 구현 방식이 달라 코드가 복잡해질 수 있다는 점을 새삼 느꼈습니다. 앞으로는 더 효율적이고 일관성 있는 코드 구조를 고민해야겠다고 생각했습니다.
- 이태호 : 데이터를 정리하고 분석하는 과정에서 생각보다 많은 시간과 세심함이 필요하다는 걸 느꼈습니다.
전기차 등록 추세가 지역별로 다르게 나타난다는 점이 흥미로웠고, 그 배경을 유추해보는 것도 재미있었습니다.
단순한 숫자보다 그 안에 숨은 의미를 파악하는 게 데이터 분석의 핵심이라는 걸 다시 한 번 깨달았습니다.
- 양진아 : 
- 황혜진 : 표면적으로는 단순한 통계처럼 보여도, 실제로 데이터를 수집하고 정리하는 과정은 시간도 오래 걸리고, 복잡한 작업이라는 걸 실감했습니다.
