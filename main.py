from domain.economy.create_df import EconomyDfCreator as edc

if __name__ == '__main__':
    economy_df = edc.create_economy()
    bank_finance_df = edc.create_bank_finance()
    income_expense_df = edc.create_income_expense()
