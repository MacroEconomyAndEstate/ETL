CREATE SCHEMA analytics;

CREATE TABLE analytics.region (
    code VARCHAR(10) NOT NULL,
    name VARCHAR(64) NOT NULL,
    PRIMARY KEY (code),
    UNIQUE (code)
) SORTKEY(code);

CREATE TABLE analytics.leading_50 (
    date DATE NOT NULL,
    leading_50_index FLOAT NOT NULL,
    PRIMARY KEY (date)
) SORTKEY (date);

CREATE TABLE analytics.monthly_real_estate (
    date DATE NOT NULL ,
    region_code VARCHAR(10) NOT NULL,
    apartment_sales_price_index FLOAT,
    apartment_lease_price_index FLOAT,
    apartment_monthly_rent_price_index FLOAT,
    apartment_sales_average_price FLOAT,
    apartment_sales_average_price_per_square_meter FLOAT,
    apartment_sales_median_price FLOAT,
    apartment_lease_average_price FLOAT,
    apartment_lease_average_price_per_square_meter FLOAT,
    apartment_lease_median_price FLOAT,
    apartment_lease_to_purchase_price_ratio FLOAT,
    buyers_dominance_index FLOAT,
    sales_transaction_activity_index FLOAT,
    lease_supply_demand_index FLOAT,
    lease_transaction_activity_index FLOAT,
    sales_price_outlook_index FLOAT,
    lease_price_outlook_index FLOAT,
    PRIMARY KEY (date, region_code),
    FOREIGN KEY (region_code) REFERENCES analytics.region (code)
) SORTKEY (date);


CREATE TABLE analytics.pir (
    date DATE NOT NULL,
    region_code VARCHAR(10) NOT NULL,
    housing_tier INT NOT NULL,
    income_tier INT NOT NULL,
    pir FLOAT,
    jpir FLOAT,
    PRIMARY KEY (date, region_code, housing_tier, income_tier),
    FOREIGN KEY (region_code) REFERENCES analytics.region (code)
) SORTKEY (date);


CREATE TABLE analytics.quarterly_real_estate (
    date DATE NOT NULL,
    region_code VARCHAR(10) NOT NULL,
    kb_apartment_pir FLOAT,
    housing_price INT,
    household_income INT,
    potential_index FLOAT,
    monthly_household_income FLOAT,
    mortgage_interest_rate FLOAT,
    total_apartment_inventory FLOAT,
    available_apartment_inventory FLOAT,
    affordable_housing_price FLOAT,
    annual_affordable_housing_cost FLOAT,
    PRIMARY KEY (date, region_code),
    FOREIGN KEY (region_code) references analytics.region (code)
) SORTKEY (date);

CREATE TABLE analytics.population (
    date DATE NOT NULL,
    region_code VARCHAR(10) NOT NULL,
    below10 FLOAT,
    teenagers FLOAT,
    twenties FLOAT,
    thirties FLOAT,
    forties FLOAT,
    fifties FLOAT,
    sixties FLOAT,
    seventies FLOAT,
    eighties FLOAT,
    nineties FLOAT,
    over_100 FLOAT,
    total_move_in INT,
    total_move_out INT,
    net_move INT,
    inner_move INT,
    inner_move_in INT,
    inner_move_out INT,
    between_move_in INT,
    between_move_out INT,
    born FLOAT,
    born_rate FLOAT,
    marriage FLOAT,
    marriage_rate FLOAT,
    public_vehicle FLOAT,
    private_vehicle FLOAT,
    commercial_vehicle FLOAT,
    total_vehicle FLOAT,
    PRIMARY KEY (date, region_code),
    FOREIGN KEY (region_code) references analytics.region (code)
) SORTKEY (date);

CREATE TABLE analytics.bank_finance (
    date DATE NOT NULL,
    household_credit FLOAT,
    demand_deposit_turnover_rate FLOAT,
    saving_deposit_turnover_rate FLOAT,
    standard_interest_rate FLOAT,
    usa_interest_rate FLOAT,
    saving_interest_rate_new FLOAT,
    saving_interest_rate_balance FLOAT,
    fixed_loan_interest_rate_new FLOAT,
    variable_loan_interest_rate_new FLOAT,
    lease_loan_interest_rate_new FLOAT,
    fixed_loan_interest_rate_balance FLOAT,
    variable_loan_interest_rate_balance FLOAT,
    lease_loan_interest_rate_balance FLOAT,
    loan_demand FLOAT,
    PRIMARY KEY (date)
) SORTKEY (date);

CREATE TABLE analytics.economy (
    date DATE NOT NULL,
    real_gdp FLOAT,
    gdp_deflator_rate FLOAT,
    leading_composite_index FLOAT,
    coincident_composite_index FLOAT,
    leading_composite_rate FLOAT,
    coincident_composite_rate FLOAT,
    PRIMARY KEY (date)
) SORTKEY (date);

CREATE TABLE analytics.income_expense (
    date DATE NOT NULL,
    nominal_gni FLOAT,
    real_gni FLOAT,
    gini_coefficient FLOAT,
    nominal_durable_goods_expense FLOAT,
    real_durable_goods_expense FLOAT,
    nominal_semi_durable_goods_expense FLOAT,
    real_semi_durable_goods_expense FLOAT,
    nominal_non_durable_goods_expense FLOAT,
    real_non_durable_goods_expense FLOAT,
    PRIMARY KEY (date)
) SORTKEY (date);

CREATE TABLE analytics.apartment_sales_price (
	date DATE NOT NULL,
	region_code VARCHAR(10),
	price INT,
	build_year INT,
	square_meter_area FLOAT,
	PRIMARY KEY (date),
    FOREIGN KEY (region_code) references analytics.region (code)
) SORTKEY (date);
