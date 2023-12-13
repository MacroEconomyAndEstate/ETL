import os
import pandas as pd
from PublicDataReader import Ecos


class EconomyDfCreator:
    def __init__(self) -> None:
        pass


    def convert_to_datetime(self, df, cycle):
        year = df.str[:4]
        if cycle == 'Q':
            quarter_to_month = {'Q1': '03-01', 'Q2': '06-01', 'Q3': '09-01', 'Q4': '12-01'}
            return pd.to_datetime(year+ '-' + df.str[4:].map(quarter_to_month), format='%Y-%m-%d')
        elif cycle == 'M':
            return pd.to_datetime(year + '-' + df.str[4:] + '-01', format='%Y-%m-%d')
        elif cycle == 'D':
            return pd.to_datetime(year + '-' + df.str[4:6] + '-' + df.str[6:], format='%Y-%m-%d')
        elif cycle == 'A':
            return pd.to_datetime(year + '-12-01', format='%Y-%m-%d')
    

    def return_final_df(self, var_name, code, cycle, start, end, code1, code2=None):
        df = Ecos(os.getenv('ECOS_SERVICE_KEY')).get_statistic_search(통계표코드=code, 주기=cycle, 검색시작일자=start, 검색종료일자=end, 통계항목코드1=code1, 통계항목코드2=code2, translate=False)
        df['TIME'] = self.convert_to_datetime(df['TIME'], cycle)
        df.rename(columns={"DATA_VALUE":var_name}, inplace=True)
        df = pd.DataFrame(df, columns=["TIME", var_name])
        df.set_index("TIME", drop=True, append=False, inplace=True)
        return df


    def create_economy(self):
        real_GDP = self.return_final_df("real_GDP", "200Y002", "Q", "1960Q2", "2023Q3", "10111")
        GDP_deflator_rate = self.return_final_df("GDP_deflator_rate", "200Y002", "Q", "1961Q1", "2023Q3", "301")
        
        leading_composite_index = self.return_final_df("leading_composite_index", "901Y067", "M", "197001", "202310", "I16A")
        coincident_composite_index = self.return_final_df("coincident_composite_index", "901Y067", "M", "197001", "202310", "I16B")
        leading_composite_rate = self.return_final_df("leading_composite_rate", "901Y067", "M", "197001", "202310", "I16E")
        coincident_composite_rate = self.return_final_df("leading_composite_rate", "901Y067", "M", "197001", "202310", "I16D")
        
        return pd.concat([real_GDP, GDP_deflator_rate, leading_composite_index, coincident_composite_index, leading_composite_rate, coincident_composite_rate], axis=1)


    def create_bank_finance(self):
        household_credit = self.return_final_df("household_credit", "151Y004", "Q", "2005Q4", "2023Q3", "11100A0")
        
        demand_deposit_turnover_rate = self.return_final_df("demand_deposit_turnover_rate", "104Y017", "M", "198501", "202309", "BDFA1")
        saving_deposit_turnover_rate = self.return_final_df("saving_deposit_turnover_rate", "104Y017", "M", "198501", "202309", "BDFA2")
        
        standard_interest_rate = self.return_final_df("standard_interest_rate", "722Y001", "D", "19990506", "20231204", "0101000")
        
        usa_interest_rate = self.return_final_df("usa_interest_rate", "902Y006", "M", "195407", "202310", "US")
        
        saving_interest_rate_new = self.return_final_df("saving_interest_rate_new", "121Y002", "M", "199601", "202310", "BEABAA21")
        
        saving_interest_rate_balance = self.return_final_df("saving_interest_rate_balance", "121Y013", "M", "200109", "202310", "BEABAB211")
        
        fixed_loan_interest_rate_new = self.return_final_df("fixed_loan_interest_rate_new", "121Y006", "M", "201301", "202310", "BECBLA030201")
        variable_loan_interest_rate_new = self.return_final_df("variable_loan_interest_rate_new", "121Y006", "M", "201301", "202310", "BECBLA030202")
        lease_loan_interest_rate_new = self.return_final_df("lease_loan_interest_rate_new", "121Y006", "M", "201501", "202310", "BECBLA03041")
        
        fixed_loan_interest_rate_balance = self.return_final_df("fixed_loan_interest_rate_balance", "121Y015", "M", "201301", "202310", "BECBLB020208")
        variable_loan_interest_rate_balance = self.return_final_df("variable_loan_interest_rate_balance", "121Y015", "M", "201301", "202310", "BECBLB020209")
        lease_loan_interest_rate_balance = self.return_final_df("lease_loan_interest_rate_balance", "121Y015", "M", "201501", "202310", "BECBLB020210")
        
        loan_demand = self.return_final_df("loan_demand", "514Y003", "Q", "2002Q1", "2023Q4", "CC03")
        
        return pd.concat([household_credit, demand_deposit_turnover_rate, saving_deposit_turnover_rate, standard_interest_rate, usa_interest_rate, saving_interest_rate_new, saving_interest_rate_balance, fixed_loan_interest_rate_new, variable_loan_interest_rate_new, lease_loan_interest_rate_new, fixed_loan_interest_rate_balance, variable_loan_interest_rate_balance, lease_loan_interest_rate_balance, loan_demand], axis=1)

    
    def create_income_expense(self):
        nominal_GNI = self.return_final_df("nominal_GNI", "200Y002", "Q", "1961Q1", "2023Q3", "20111")
        real_GNI = self.return_final_df("real_GNI", "200Y002", "Q", "1961Q1", "2023Q3", "20112")
        
        gini_coefficient = self.return_final_df("gini_coefficient", "901Y031", "A", "2011", "2021", "I38A", "10")
        
        nominal_durable_goods_expense = self.return_final_df("nominal_durable_goods_expense", "200Y044", "Q", "1970Q1", "2023Q3", "10101")
        real_durable_goods_expense = self.return_final_df("real_durable_goods_expense", "200Y045", "Q", "1970Q1", "2023Q3", "10101")
        nominal_semi_durable_goods_expense = self.return_final_df("nominal_semi_durable_goods_expense", "200Y044", "Q", "1970Q1", "2023Q3", "10201")
        real_semi_durable_goods_expense = self.return_final_df("real_semi_durable_goods_expense", "200Y045", "Q", "1970Q1", "2023Q3", "10201")
        nominal_non_durable_goods_expense = self.return_final_df("nominal_non_durable_goods_expense", "200Y044", "Q", "1970Q1", "2023Q3", "10301")
        real_non_durable_goods_expense = self.return_final_df("real_non_durable_goods_expense", "200Y045", "Q", "1970Q1", "2023Q3", "10301")
        
        return pd.concat([nominal_GNI, real_GNI, gini_coefficient, nominal_durable_goods_expense, real_durable_goods_expense, nominal_semi_durable_goods_expense, real_semi_durable_goods_expense, nominal_non_durable_goods_expense, real_non_durable_goods_expense], axis=1)