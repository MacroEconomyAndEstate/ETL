from PublicDataReader import Kbland
import pandas as pd
from pandas import DataFrame


class RealEstateDataProcessor:
    def __init__(self):
        self.api = Kbland()

    def get_monthly_real_estate_df(self) -> DataFrame:
        df1 = self.api.get_price_index("01", "01", "01")
        df1 = df1[['날짜', '지역코드', '가격지수']]
        df1 = df1.rename(columns={'가격지수': 'apartment_sale_price_index'})

        df2 = self.api.get_price_index("01", "01", "02")
        df2 = df2[['날짜', '지역코드', '가격지수']]
        df2 = df2.rename(columns={'가격지수': 'apartment_lease_price_index'})

        df3 = self.api.get_monthly_apartment_wolse_index()
        df3 = df3[['날짜', '지역코드', '가격지수']]
        df3 = df3.rename(columns={'가격지수': 'apartment_monthly_rent_price_index'})

        df4 = self.api.get_average_price("01", "01")
        df4 = df4[['날짜', '지역코드', '평균가격']]
        df4 = df4.rename(columns={'평균가격': 'apartment_sales_average_price'})

        df5 = self.api.get_average_price_per_squaremeter("01", "01")
        df5 = df5[['날짜', '지역코드', '㎡당 평균가격']]
        df5 = df5.rename(columns={'㎡당 평균가격': 'apartment_sales_average_price_per_square_meter'})

        df6 = self.api.get_median_price("01", "01")
        df6 = df6[['날짜', '지역코드', '중위가격']]
        df6 = df6.rename(columns={'중위가격': 'apartment_sales_median_price'})

        df7 = self.api.get_average_price("01", "02")
        df7 = df7[['날짜', '지역코드', '평균가격']]
        df7 = df7.rename(columns={'평균가격': 'apartment_lease_average_price'})

        df8 = self.api.get_average_price_per_squaremeter("01", "02")
        df8 = df8[['날짜', '지역코드', '㎡당 평균가격']]
        df8 = df8.rename(columns={'㎡당 평균가격': 'apartment_lease_average_price_per_square_meter'})

        df9 = self.api.get_median_price("01", "02")
        df9 = df9[['날짜', '지역코드', '중위가격']]
        df9 = df9.rename(columns={'중위가격': 'apartment_lease_median_price'})

        df10 = self.api.get_jeonse_price_ratio("01")
        df10 = df10[['날짜', '지역코드', '전세가격비율']]
        df10 = df10.rename(columns={'전세가격비율': 'apartment_lease_to_purchase_price_ratio'})

        df_list = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10]
        merged_df = df_list[0].reset_index(drop=True)
        for i, df in enumerate(df_list[1:]):
            df = df.reset_index(drop=True)
            merged_df = pd.merge(merged_df, df, on=["날짜", "지역코드"], how='outer')
        merged_df.rename(columns={"날짜": "date", "지역코드": "region_code"}, inplace=True)

        return merged_df

    def get_leading_50_df(self) -> DataFrame:
        df = self.api.get_lead_apartment_50_index()
        df = df[['날짜', '선도50지수']]
        df.rename(columns={'날짜': 'date', '선도50지수': 'leading_50_index'})
        return df

    def get_pir_df(self) -> DataFrame:
        df1 = self.api.get_pir("01")
        df1 = df1[['지역코드', '주택분위', '소득분위', '날짜', 'PIR']]
        df1.rename(columns={'PIR': 'pir_index'}, inplace=True)

        df2 = self.api.get_pir("02")
        df2 = df2[['지역코드', '주택분위', '소득분위', '날짜', 'PIR']]
        df2.rename(columns={'PIR': 'jpir_index'}, inplace=True)

        merged_df = pd.merge(df1, df2, on=['지역코드', '주택분위', '소득분위', '날짜'], how='outer')
        merged_df.rename(columns={'날짜': 'date', '지역코드': 'region_code', '주택분위': 'housing_tier', '소득분위': 'income_tier'},
                         inplace=True)
        return merged_df

    def get_quarterly_real_estate_df(self) -> DataFrame:
        df1 = self.api.get_apartment_mortgage_loan_pir()
        df1 = df1[['지역코드', '날짜', 'KB아파트PIR', '주택가격', '가구소득']]

        df2 = self.api.get_kb_housing_purchase_potential_index()
        df2 = df2[['지역코드', '날짜', '잠재력지수', '가구별월소득금액', '주택담보대출금리', '총아파트재고량', '구입가능아파트재고량', '구입가능주택가격', '연간지출가능주거비용']]

        merged_df = pd.merge(df1, df2, on=['지역코드', '날짜'])
        merged_df.rename(
            columns={"날짜": "date",
                     "지역코드": "region_code",
                     "KB아파트PIR": 'kb_apartment_pir',
                     "주택가격": "housing_price",
                     "가구소득": "household_income",
                     "잠재력지수": "potential_index",
                     "가구별월소득금액": "monthly_household_income",
                     "주택담보대출금리": "mortgage_interest_rate",
                     "총아파트재고량": "total_apartment_inventory",
                     '구입가능아파트재고량': "available_apartment_inventory",
                     '구입가능주택가격': "affordable_housing_price",
                     '연간지출가능주거비용': "annual_affordable_housing_cost"
                     },
            inplace=True)
        return merged_df
