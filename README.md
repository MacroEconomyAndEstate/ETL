# 프로젝트 개요

### 주제
DW & BI 구축을 통한 거시 경제 흐름과 부동산 시장 간 패턴 파악, 부동산 시장과 경제지표와의 상관관계 시각화
### 기간
2023.12.04 ~ 2023.12.08
### 팀원
|  | 역할                        |
| --- |---------------------------|
| 이예인 | AWS S3 및 Redshift 구축, DB 모델링, 부동산 지표 ETL 및 시각화|
| 김원경 | 주제 선정 및 사용할 데이터 구체화, 데이터 소스 조사, 경제 지표 ETL 및 시각화|
| 김형후 | Preset 대시보드 구축, 데이터 소스 조사, 아파트 매매 실거래가 ETL|
| 조서희 | 데이터 소스 조사, 인구 지표 ETL 및 시각화|

# 프로젝트 상세
### 아키텍처
![Untitled.png](..%2F..%2FDownloads%2FUntitled.png)
### ERD
![estate-erd.png](..%2F..%2FDownloads%2Festate-erd.png)
### 사용한 데이터
- 부동산 지표
  [KB부동산 데이터허브](https://data.kbland.kr/)
- 경제 지표
  [한국은행 Open API 서비스](https://ecos.bok.or.kr/api/#/DevGuide/StatisticalCodeSearch)
- 인구 
  - 취업
    [지표서비스 | e-나라지표](https://www.index.go.kr/unity/potal/main/EachDtlPageDetail.do?idx_cd=1063)
  - 인구 이동 [KOSIS](https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1B26001_A01&conn_path=I2), 
[통신 모바일 인구 이동량](http://bigdata.kostat.go.kr/foresight/mobMoventSido.do?isBigmain=y)
  - 출생 사망 통계 [KOSIS](https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1B8000G)
  - 자동차 등록 현황 [국가교통데이터베이스](https://www.ktdb.go.kr/www/selectTrnsportTreeView.do?key=32)
- 아파트 실거래가 [국토교통부_아파트매매 실거래자료](https://www.data.go.kr/data/15058747/openapi.do)
- 지역 [법정동코드목록조회 - 준코드관리시스템](https://www.code.go.kr/stdcode/regCodeL.do)
### 기술 스택 및 선정 이유
### 고민했던 점
- planning hint로 사용되는 것을 고려해 테이블 설계했습니다.
    - 데이터를 INSERT할 때는 PK, FK 무결성이 보장되지 않습니다.
      - [테이블 제약 조건 정의 - Amazon Redshift](https://docs.aws.amazon.com/ko_kr/redshift/latest/dg/t_Defining_constraints.html)
    - Preset에서 FK를 가진 테이블을 불러오지 못하는 문제가 있어 대시보드 시각화시 FK를 제거하고 진행했습니다.
- 대부분 시계열 데이터를 시각화하는 프로젝트의 특성을 고려해 모든 테이블에 SORT KEY로 date 지정했습니다.
- 다음과 같은 이유로 월별 데이터를 year과 month 두 컬럼으로 나눠 int 형으로 저장 vs date 형으로 하나만 저장하는 방법 사이에서 date 형을 저장하는 방법을 선택했습니다:
    - year과 month 두 컬럼으로 나누는 방식은 8byte(4byte x 2) 필요, date형은 4byte만 필요해 용량을 줄일 수 있습니다.
    - date형으로 저장시에, SQL에서 날짜 계산이 용이합니다.
    - 다른 테이블과 date를 join하기에 용이합니다.
- EC2에 Suerpet을 Docker Compose로 띄우려 했으나, 메모리가 8기가 이상 필요하다는 문제가 있었습니다.
    - AWS 프리티어가 제공하는 EC2 사양은 RAM 1GB로 Superset을 띄우기에 부족했습니다.
    - Superset을 SaaS 형태로 제공하는 Preset을 사용해 해결했습니다.
### 보완할 점
- Preset에서 FK가 있는 데이터셋이 불러와지지 않는 문제가 있었습니다.
    - 정확한 원인 파악이 어려워 FK를 임의로 제거하고 데이터셋을 생성했습니다.
- 크롤링 자동화 및 S3 업로드 자동화, AUTO COPY가 필요합니다.
- Redshift 비용 문제로 인한 데이터웨어하우스 변경이  필요합니다.
- 분석 대시보드 맞춤 디비 모델링이 필요합니다.
    - raw data를 그대로 저장(ETL)하고, 이를 분석 대시보드에 맞게 ELT 하는 과정으로 변경
- 시각화 시나리오에 대한 고민 없이 크롤링부터 시작해 사용하지 않는 데이터가 존재합니다.
    - 시나리오를 명확히 정의한 뒤 데이터를 수집하는 과정이 필요합니다.
- 인구 데이터에서 일부 기간에 대해 전국 인구의 총합이 1000만인 부정확성을 발견했습니다.
# 데모