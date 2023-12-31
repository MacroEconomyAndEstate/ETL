import pandas as pd

class MoveDataProcessor:
    def __init__(self, file_path):
        self.move = pd.read_csv(file_path)
        self.move.rename(columns={'시점': '연월'}, inplace=True)
        self.time = self._preprocess_time()
        self.regions = self._split_regions()
        self.lst = ['전국', '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시',
                    '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원특별자치도',
                    '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도']
        self.result = self._process_data()

    def _preprocess_time(self):
        time = self.move.pop('연월')
        time.columns = time.iloc[0]
        time = time[1:].reset_index(drop=True)
        return time

    def _split_regions(self):
        regions = []
        for i in range(0, self.move.shape[1], 8):
            region_data = self.move.iloc[:, i:i+8].copy()
            regions.append(region_data)
        return regions

    def _process_data(self):
        df_list = []
        for i, region_data in enumerate(self.regions):
            region_data.columns = region_data.iloc[0]
            region_data = region_data[1:].reset_index(drop=True)
            region_data['행정구역'] = self.lst[i]
            region_data = pd.concat([region_data['행정구역'], region_data.drop('행정구역', axis=1)], axis=1)
            region_data = pd.concat([self.time, region_data], axis=1)
            df_list.append(region_data)
        result_df = pd.concat(df_list, ignore_index=True)
        result_df['연월'] = pd.to_datetime(result_df['연월'], format='%Y.%m')
        columns_to_convert = result_df.columns[3:]
        result_df[columns_to_convert] = result_df[columns_to_convert].astype(int)
        return result_df

    def save_result_csv(self, file_path='이동인구.csv'):
        self.result.to_csv(file_path, index=False)

# Example Usage:
file_path = 'move.csv'
move_processor = MoveDataProcessor(file_path)
move_processor.save_result_csv()



class LifeDataProcessor:
    def __init__(self, file_path):
        self.life = pd.read_csv(file_path, encoding='CP949').transpose().reset_index()
        self.time = self._preprocess_time()
        self.regions = self._split_regions()
        self.lst = ['전국', '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시',
                    '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원특별자치도',
                    '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도']
        self.result = self._process_data()

    def _preprocess_time(self):
        time = self.life.pop('index')
        time = time[4:].reset_index(drop=True)
        return time

    def _split_regions(self):
        regions = []
        for i in range(0, self.life.shape[1], 11):
            region_data = self.life.iloc[:, i:i+11].copy()
            regions.append(region_data)
        return regions

    def _process_data(self):
        df_list = []
        for i, region_data in enumerate(self.regions):
            region_data.columns = region_data.iloc[1]
            region_data = region_data[4:].reset_index(drop=True)
            region_data['행정구역'] = self.lst[i]
            region_data = pd.concat([region_data['행정구역'], region_data.drop('행정구역', axis=1)], axis=1)
            region_data = pd.concat([self.time, region_data], axis=1)
            df_list.append(region_data)
        result_df = pd.concat(df_list, ignore_index=True)
        result_df['index'] = pd.to_datetime(result_df['index'], format='%Y.%m 월', errors='coerce')
        result_df.dropna(subset=['index'], inplace=True)
        selected_columns = result_df.select_dtypes(include='object').columns[1:]
        result_df[selected_columns] = result_df[selected_columns].applymap(pd.to_numeric, errors='coerce')
        result_df = result_df.drop(['자연증가건수(명)', '자연증가율(천명당)'], axis=1)
        result_df = result_df.drop(['사망자수(명)', '조사망률(천명당)', '이혼건수(건)', '조이혼율(천명당)', '합계출산율'], axis=1)
        result_df.rename(columns={'index': '연월'}, inplace=True)
        return result_df

    def save_result_csv(self, file_path='출생혼인인구.csv'):
        self.result.to_csv(file_path, index=False)

# Example Usage:
file_path_life = 'life.csv'
life_processor = LifeDataProcessor(file_path_life)
life_processor.save_result_csv()



class CarDataProcessor:
    def __init__(self, file_path):
        self.car = pd.read_csv(file_path, encoding='CP949')
        self.year = self.car.pop('구분1')
        self.month = self.car.pop('시도별')
        self.regions = self._split_regions()
        self.lst = ['전국', '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시',
                    '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원특별자치도',
                    '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도']
        self.result = self._process_data()

    def _split_regions(self):
        regions = []
        for i in range(0, self.car.shape[1], 20):
            region_data = self.car.iloc[:, i:i+20].copy()
            regions.append(region_data)
        return regions

    def _process_data(self):
        df_list = []
        for i, region_data in enumerate(self.regions):
            region_data.columns = region_data.iloc[1]
            region_data = region_data[:].reset_index(drop=True)
            region_data['행정구역'] = self.lst[i]
            region_data = pd.concat([self.year, self.month, region_data], axis=1)
            df_list.append(region_data)
        result_df = pd.concat(df_list, ignore_index=True)
        result_df = result_df.iloc[2:, :].copy()
        new_columns = ['연도', '월', '행정구역', 
                       '전체(관용)', '전체(자가용)', '전체(영업용)', '전체(계)', 
                       '승용(관용)', '승용(자가용)', '승용(영업용)', '승용(계)',
                       '승합(관용)', '승합(자가용)', '승합(영업용)', '승합(계)', 
                       '화물(관용)', '화물(자가용)', '화물(영업용)', '화물(계)', 
                       '특수(관용)', '특수(자가용)', '특수(영업용)', '특수(계)']
        result_df.columns = new_columns
        result_df['연도'] = result_df['연도'].str[:4]
        result_df['월'] = result_df['월'].str[:-1]
        result_df.dropna(subset=['전체(관용)'], inplace=True)
        to_int = result_df.select_dtypes(include='object').columns[:2]
        result_df[to_int] = result_df[to_int].applymap(pd.to_numeric, errors='coerce')
        result_df['연도'] = pd.to_numeric(result_df['연도'], errors='coerce').astype('Int64')
        result_df['월'] = pd.to_numeric(result_df['월'], errors='coerce').astype('Int64')
        result_df = result_df.dropna()
        result_df['연월'] = pd.to_datetime(result_df[['연도', '월']].astype(str).agg('-'.join, axis=1))
        result_df = result_df.drop(['연도', '월'], axis=1)
        result_df = pd.concat([result_df['연월'], result_df.iloc[:, :-1]], axis=1)
        result_df = result_df.iloc[:, :6]
        return result_df

    def save_result_csv(self, file_path='차량등록인구.csv'):
        self.result.to_csv(file_path, index=False)

# Example Usage:
file_path_car = 'car.csv'
car_processor = CarDataProcessor(file_path_car)
car_processor.save_result_csv()


class PopulationDataProcessor:
    def __init__(self, move_file, job_file, life_file, car_file):
        self.move = pd.read_csv(move_file)
        self.job = pd.read_csv(job_file)
        self.life = pd.read_csv(life_file)
        self.car = pd.read_csv(car_file)

    def _filter_data(self):
        cond1 = self.car['연월'] >= '2014-01-01'
        cond2 = self.life['연월'] <= '2023-04-01'
        cond3 = self.move['연월'] <= '2023-04-01'

        self.car = self.car[cond1].reset_index().drop('index', axis=1)
        self.life = self.life[cond2].reset_index().drop('index', axis=1)
        self.move = self.move[cond3].reset_index().drop('index', axis=1)

    def _concat_data(self):
        df = pd.concat([self.move, self.life.iloc[:, 2:], self.car.iloc[:, 2:]], axis=1)
        new_columns = ['date', 'region', 'total_movein', 'total_moveout', 'net_move',
                       'inner_move', 'inner_movein', 'inner_moveout', 'between_movein',
                       'between_moveout', 'born', 'born_rate', 'marriage', 'marriage_rate',
                       'public_vehicle', 'private_vehicle', 'commercial_vehicle', 'total_vehicle']
        df.columns = new_columns
        return df

    def save_combined_data(self, output_file='population.csv'):
        self._filter_data()
        result_df = self._concat_data()
        result_df.to_csv(output_file, index=False)

# Example Usage:
move_file = '이동인구.csv'
job_file = '취업인구.csv'
life_file = '출생혼인인구.csv'
car_file = '차량등록인구.csv'

population_processor = PopulationDataProcessor(move_file, job_file, life_file, car_file)
population_processor.save_combined_data()


class PopulationDataProcessor:
    def __init__(self, move_file, job_file, life_file, car_file):
        self.move = pd.read_csv(move_file)
        self.job = pd.read_csv(job_file)
        self.life = pd.read_csv(life_file)
        self.car = pd.read_csv(car_file)

    def _filter_data(self):
        cond1 = self.car['연월'] >= '2014-01-01'
        cond2 = self.life['연월'] <= '2023-04-01'
        cond3 = self.move['연월'] <= '2023-04-01'

        self.car = self.car[cond1].reset_index().drop('index', axis=1)
        self.life = self.life[cond2].reset_index().drop('index', axis=1)
        self.move = self.move[cond3].reset_index().drop('index', axis=1)

    def _concat_data(self):
        df = pd.concat([self.move, self.life.iloc[:, 2:], self.car.iloc[:, 2:]], axis=1)
        new_columns = ['date', 'region', 'total_movein', 'total_moveout', 'net_move',
                       'inner_move', 'inner_movein', 'inner_moveout', 'between_movein',
                       'between_moveout', 'born', 'born_rate', 'marriage', 'marriage_rate',
                       'public_vehicle', 'private_vehicle', 'commercial_vehicle', 'total_vehicle']
        df.columns = new_columns
        return df

    def _clean_data(self, df):
        df['date'] = pd.to_datetime(df['date'])
        df['public_vehicle'] = df['public_vehicle'].str.replace(',', '').astype(float)
        df['private_vehicle'] = df['private_vehicle'].str.replace(',', '').astype(float)
        df['commercial_vehicle'] = df['commercial_vehicle'].str.replace(',', '').astype(float)
        df['total_vehicle'] = df['total_vehicle'].str.replace(',', '').astype(float)
        return df

    def save_combined_data(self, output_file='population.csv'):
        self._filter_data()
        result_df = self._concat_data()
        result_df = self._clean_data(result_df)
        result_df.to_csv(output_file, index=False)

# Example Usage:
move_file = '이동인구.csv'
job_file = '취업인구.csv'
life_file = '출생혼인인구.csv'
car_file = '차량등록인구.csv'

population_processor = PopulationDataProcessor(move_file, job_file, life_file, car_file)
population_processor.save_combined_data()


class InsertRegionCode:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.region_codes = {
            '전국': '0000000000',
            '서울특별시': '1100000000',
            '경상남도': '4800000000',
            '경상북도': '4700000000',
            '전라남도': '4600000000',
            '전라북도': '4500000000',
            '충청남도': '4400000000',
            '충청북도': '4300000000',
            '강원특별자치도': '5100000000',
            '경기도': '4100000000',
            '세종특별자치시': '3611000000',
            '울산광역시': '3100000000',
            '대전광역시': '3000000000',
            '광주광역시': '2900000000',
            '인천광역시': '2800000000',
            '대구광역시': '2700000000',
            '부산광역시': '2600000000',
            '제주특별자치도': '5000000000'
        }

    def process_data(self):
        self.df['area_code'] = self.df['region'].map(self.region_codes)
        self.df['area_code'] = self.df['area_code'].astype(str).str.zfill(10)
        self.df = pd.concat([self.df.iloc[:, :2], self.df['area_code'], self.df.iloc[:, 2:-1]], axis=1)

    def save_to_csv(self, output_path='final_population.csv'):
        self.df.to_csv(output_path, index=False)

    def display_info(self):
        print(self.df.info())
        print(self.df.columns)


# 사용 예시
data_processor = InsertRegionCode('population.CSV')
data_processor.process_data()
data_processor.display_info()
data_processor.save_to_csv()
