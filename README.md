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
![Untitled](https://github.com/MacroEconomyAndEstate/ETL/assets/39490214/9cdcb4f9-db95-43b1-8d59-75fbbb403a8d)

### ERD
![estate-erd](https://github.com/MacroEconomyAndEstate/ETL/assets/39490214/85cb3410-9552-4aab-a8cf-8a7ba5039626)

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
- planning hint로 사용되는 것을 고려해 테이블 설계
    - 데이터를 INSERT할 때는 PK, FK 무결성이 보장되지 않음
      [테이블 제약 조건 정의 - Amazon Redshift](https://docs.aws.amazon.com/ko_kr/redshift/latest/dg/t_Defining_constraints.html)
    - 하지만 Preset에서 FK를 가진 테이블을 불러오지 못하는 문제로 대시보드 시각화시 FK를 제거하고 진행
- 대부분 시계열 데이터를 시각화하는 프로젝트의 특성을 고려해 모든 테이블에 SORT KEY로 date 지정
- 월별 데이터를 year과 month 두 컬럼으로 나눠 int 형으로 저장 vs date 형으로 하나만 저장하는 방법 사이에서 date 형을 저장하는 방법을 선택
    - year과 month 두 컬럼으로 나누는 방식은 8byte(4byte x 2) 필요, date형은 4byte만 필요
    - date형으로 저장시에, SQL에서 날짜 계산이 용이
    - 다른 테이블과 date를 join하기에 용이
- EC2에 Suerpet을 Docker Compose로 띄우려 했으나, 메모리가 8기가 이상 필요
    - AWS 프리티어가 제공하는 EC2 사양은 RAM 1GB로 Superset을 띄우기에 부족
    - Superset을 SaaS 형태로 제공하는 Preset을 사용해 해결
### 보완할 점
- Preset에서 FK가 있는 데이터셋이 불러와지지 않는 문제
    - FK를 임의로 제거하고 데이터셋을 생성
- 크롤링 자동화 및 S3 업로드 자동화, AUTO COPY
- Redshift 비용 문제로 인한 데이터웨어하우스 변경
- 분석 대시보드 맞춤 디비 모델링
    - raw data를 그대로 저장(ETL)하고, 이를 분석 대시보드에 맞게 ELT 하는 과정 필요
- 시각화 시나리오에 대한 고민 없이 크롤링부터 시작해 사용하지 않는 데이터가 존재
    - 시나리오를 명확히 정의한 뒤 데이터를 크롤링했으면 낭비되는 데이터가 없었을 것 같다.
- 인구 데이터의 부정확성
