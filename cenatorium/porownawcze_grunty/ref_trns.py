from sqlalchemy import create_engine
from config import DB_URI
import numpy as np
from datetime import datetime
from abc import abstractmethod, ABC
import pandas as pd
from sqlalchemy.sql import text
from sqlalchemy import create_engine

conn = create_engine(DB_URI)

# 52.166864389009426, 20.84524408978703
input_parameters = {'geo_lon': 21.00193,
       'geo_lat': 52.335899,
       'tr_ref_count': 20,
       'data_wyceny': '2022-01-01',
       'teryt': '1465038',
       'suma_powierzchni_dzialek': 1000,
       #'data_referencyjna': '2020-01-01',
       'final_price': 300}

input_parameters = {'geo_lon': 21.168886,
       'geo_lat': 52.405435,
       'tr_ref_count': 20,
       'data_wyceny': '2018-04-01',
       'teryt': '1434011',
       'suma_powierzchni_dzialek': 573.0,
       #'data_referencyjna': '2020-01-01',
       'final_price': 300}

#52.405435	21.168886	573.0


search = {'lon': input_parameters['geo_lon'],
                'lat': input_parameters['geo_lat'],
                'powiat_id': input_parameters['teryt'][:4],
                'valuation_date': input_parameters['data_wyceny'],
                'final_price': input_parameters['final_price'],
                #'min_reference_date': input_parameters['data_referencyjna'],
                'max_price': input_parameters['final_price'] * 1.4,
                'min_price': input_parameters['final_price'] * 0.6,
                'area': input_parameters['suma_powierzchni_dzialek'],
                'area_min': input_parameters['suma_powierzchni_dzialek'] * 0.75,
                'area_max': input_parameters['suma_powierzchni_dzialek'] * 1.5}


# class Ref(ABC):
#     def __init__(self, con: create_engine, input_parameters: dict):
#         self.conn = con
#         self._geo_lat = input_parameters['geo_lat']
#         self._geo_lon = input_parameters['geo_lon']
#         self._final_price = input_parameters['final_price']
#         self._teryt = input_parameters['teryt']
#
#
#         self._create_distance_cost_importance_attribute(input_parameters, default_importance=3)
#         self._create_date_cost_importance_attribute(input_parameters, default_importance=3)
#
#         self._create_tr_ref_count_attribute(input_parameters)
#         self._min_tr_ref_good_count = 10
#         self._powiat_id = self._teryt[:4]
#         self._area_update_max = 3000
#         self._area_update_min = 300
#         self._brt_tr_ref = []
#         self._similar_tr_df = pd.DataFrame()
#         self._search_brt_db_params = {
#             'lon': self._geo_lon,
#             'lat': self._geo_lat,
#             'powiat_id': self._powiat_id,
#             'valuation_date': self._valuation_date,
#             'final_price': self._final_price,
#             'min_reference_date': self._min_reference_date,
#             'max_price': self._final_price * (1 + self._max_percent_price / 100),
#             'min_price': self._final_price * (1 - self._max_percent_price / 100),
#             'area_min': self._area * 0.5,
#             'area_max': self._area * 2.5}





def get_sqlite_queryset(query_sql, input_parameters):
    """ Uzupelnienianie danych i wywolanie zapytania """

    stmt = text(query_sql)
    queryset = conn.execute(stmt, input_parameters)
    return queryset

def input_similar_tr_df_count(query_sql, input_parameters):
    """ Liczba transakcji do pobrania w modelu BRT """

    queryset = get_sqlite_queryset(query_sql, input_parameters)
    input_tr_count = queryset.fetchone()
    return input_tr_count[0]

def get_similar_database_from_sql(query_sql, input_parameters):
    """ Pobieranie danych do modelu BRT"""

    queryset = get_sqlite_queryset(query_sql, input_parameters)
    input_df = queryset.fetchall()
    input_df = pd.DataFrame(input_df, columns=queryset.keys())
    return input_df

# def ola(input_parameters):
#             t44t = {'lon': input_parameters['geo_lon'],
#                 'lat': input_parameters['geo_lat'],
#                 'powiat_id': input_parameters['teryt'][:4],
#                 'valuation_date': input_parameters['data_wyceny'],
#                 'final_price': input_parameters['final_price'],
#                 'min_reference_date': input_parameters['data_referencyjna'],
#                 'max_price': input_parameters['final_price'] * 1.2,
#                 'min_price': input_parameters['final_price'] * 0.8,
#                 'area_min': input_parameters['suma_powierzchni_dzialek'] * 0.5,
#                 'area_max': input_parameters['suma_powierzchni_dzialek'] * 2.5}


tr_cond_query = """
                SELECT  COUNT(*) FROM avm.avm_test_gcb_agl_waw    WHERE
                    ST_DWithin(ST_Transform(st_setsrid(st_makepoint(:lon,:lat),4326),2180), ST_Transform(st_setsrid(st_makepoint( geo_lon,geo_lat),4326),2180), 20000)
                        
                        AND data_dokumentu <= :valuation_date 
                        AND cena_m2 >= :min_price
                        AND cena_m2 <=  :max_price
                        AND powiat_id = :powiat_id 
                 """




o = input_similar_tr_df_count(
            query_sql=tr_cond_query,
            input_parameters=search)

brt_u27_unclean_query = """
        SELECT id::text,
            powiat_id::text,
            teryt::text,
            RIGHT(teryt,1)::numeric rodzaj_gminy,
            geo_lat::float,
            geo_lon::float,

            cena_m2::float,

            to_char(data_dokumentu::timestamp,'YYYY-MM-DD')  data_dokumentu,
            suma_powierzchni_dzialek::float suma_powierzchni_dzialek,
            date_part('year',
            age(:valuation_date,data_dokumentu::date))*12 +
            date_part('month',age(:valuation_date,data_dokumentu::date)) as month_diff,
            ST_Distance(ST_Transform(st_setsrid(st_makepoint( geo_lon,geo_lat),4326),2180), ST_Transform(st_setsrid(st_makepoint( :lon,:lat),4326),2180))::int as distance_m,
            ROUND(100 * ABS(1-cena_m2/:final_price), 2)::float as price_percent_diff
            
            FROM avm.avm_test_gcb_agl_waw 
            WHERE
            ST_DWithin(ST_Transform(st_setsrid(st_makepoint(:lon, :lat),4326),2180), ST_Transform(st_setsrid(st_makepoint( geo_lon,geo_lat),4326),2180), 20000)
                AND data_dokumentu <= :valuation_date AND powiat_id = :powiat_id
                AND suma_powierzchni_dzialek >= :area_min AND suma_powierzchni_dzialek <= :area_max
                  AND cena_m2 >= :min_price
                AND cena_m2 <=  :max_price"""

similar_tr_df = get_similar_database_from_sql(
            query_sql=brt_u27_unclean_query,
            input_parameters=search)


#def _update_date_cost(self):
months_6 = similar_tr_df.month_diff <= 6
months_12 = similar_tr_df.month_diff.isin(range(7, 13))
months_36 = similar_tr_df.month_diff.isin(range(13, 37))
above_36 = similar_tr_df.month_diff > 36

similar_tr_df.loc[months_6, 'date_cost'] = 10

similar_tr_df.loc[months_12, 'date_cost'] = similar_tr_df.loc[
                                                          months_12, 'month_diff'] * 2

similar_tr_df.loc[months_36, 'date_cost'] = similar_tr_df.loc[
                                                           months_36, 'month_diff'] *3
similar_tr_df.loc[above_36, 'date_cost'] =similar_tr_df.loc[
                                                           above_36, 'month_diff'] *4


#def _update_distance_m_cost(self):
distance_300m = (similar_tr_df['distance_m'] <= 300)
distance_500m = np.logical_and(similar_tr_df['distance_m'] > 300,
                               similar_tr_df['distance_m'] <= 500)
distance_1000m = np.logical_and(similar_tr_df['distance_m'] > 500,
                                similar_tr_df['distance_m'] <= 1000)

distance_1500m = np.logical_and(similar_tr_df['distance_m'] > 1000,
                                similar_tr_df['distance_m'] <= 1500)

distance_2000m = np.logical_and(similar_tr_df['distance_m'] > 1500,
                                similar_tr_df['distance_m'] <= 2000)

distance_4000m = np.logical_and(similar_tr_df['distance_m'] > 2000,
                                similar_tr_df['distance_m'] <= 4000)

distance_6000m = np.logical_and(similar_tr_df['distance_m'] > 4000,
                                similar_tr_df['distance_m'] <= 6000)
distance_10000m = np.logical_and(similar_tr_df['distance_m'] > 6000,
                            similar_tr_df['distance_m'] <= 10000)
above_10000m = (similar_tr_df['distance_m'] > 10000)




similar_tr_df.loc[
distance_300m, 'distance_m_cost'] =25
similar_tr_df.loc[distance_500m, 'distance_m_cost'] = (similar_tr_df.loc[
distance_500m, 'distance_m'] - 300) * 0.05 + 30
similar_tr_df.loc[distance_1000m, 'distance_m_cost'] = (similar_tr_df.loc[
                                                                  distance_1000m, 'distance_m'] - 500) * 0.04 + 40
similar_tr_df.loc[distance_1500m, 'distance_m_cost'] = (similar_tr_df.loc[
                                                                  distance_1500m, 'distance_m'] - 1000) * 0.06 + 60
similar_tr_df.loc[distance_2000m, 'distance_m_cost'] = (similar_tr_df.loc[
                                                                  distance_2000m, 'distance_m'] - 1500) * 0.02 + 90
similar_tr_df.loc[distance_4000m, 'distance_m_cost'] = (similar_tr_df.loc[
                                                                  distance_4000m, 'distance_m'] - 2000) * 0.025 + 100
similar_tr_df.loc[distance_6000m, 'distance_m_cost'] = (similar_tr_df.loc[
                                                                  distance_6000m, 'distance_m'] - 3000) * 0.01 + 125
similar_tr_df.loc[distance_10000m, 'distance_m_cost'] = (similar_tr_df.loc[
                                                                  distance_10000m, 'distance_m'] - 3000) * 0.012 + 125
similar_tr_df.loc[above_10000m, 'distance_m_cost'] = (similar_tr_df.loc[
                                                                  above_10000m, 'distance_m'] - 3000) * 0.014 + 125

similar_tr_df['distance_m_cost'] = np.where(
    similar_tr_df['distance_m_cost'] <= 300,
    similar_tr_df['distance_m_cost'], 300)


similar_tr_df['area_cost'] = 150 * np.abs(1 - similar_tr_df[
            'suma_powierzchni_dzialek'] /search['area'])


percent_5 = (similar_tr_df['price_percent_diff'] <= 5)
percent_10 = np.logical_and(similar_tr_df['price_percent_diff'] > 5,
                            similar_tr_df['price_percent_diff'] <= 10)
percent_15 = np.logical_and(similar_tr_df['price_percent_diff'] > 10,
                            similar_tr_df['price_percent_diff'] <= 15)
percent_20 = np.logical_and(similar_tr_df['price_percent_diff'] > 15,
                            similar_tr_df['price_percent_diff'] <= 20)
percent_above_20 = similar_tr_df['price_percent_diff'] > 20

similar_tr_df.loc[percent_5, 'price_cost'] = 10  * 4
similar_tr_df.loc[percent_10, 'price_cost'] = (similar_tr_df.loc[
                    percent_10, 'price_percent_diff'] - 5) * 5 + 50

similar_tr_df.loc[percent_15, 'price_cost'] = (similar_tr_df.loc[
                     percent_15, 'price_percent_diff'] - 10) * 3 + 75

similar_tr_df.loc[percent_20, 'price_cost'] = (similar_tr_df.loc[
             percent_20, 'price_percent_diff'] - 15) * 2 + 90

similar_tr_df.loc[percent_above_20, 'price_cost'] = (similar_tr_df.loc[
                 percent_above_20, 'price_percent_diff'] - 20) * 10 + 100
similar_tr_df['price_cost'] = np.where(
    similar_tr_df['price_cost'] <= 250,
    similar_tr_df['price_cost'], 250)

similar_tr_df['final_cost'] = np.sum([
            similar_tr_df['price_cost'].pow(2),
            similar_tr_df['area_cost'].pow(2),
            similar_tr_df['distance_m_cost'].pow(2),
            similar_tr_df['date_cost'].pow(2)
        ], axis=0)
similar_tr_df['final_cost'] = np.sqrt(similar_tr_df['final_cost'] / 7.0)

similar_tr_df =similar_tr_df.sort_values(by=['final_cost'])
similar_tr_df['final_cost'] = np.round(similar_tr_df['final_cost'], 4)






# class Reftr(ABC):
#
#        def __init__(self, con: create_engine, input_parameters: dict):
#               self.conn = con
#               self._geo_lat = input_parameters['geo_lat']
#               self._geo_lon = input_parameters['geo_lon']
#               self._final_price = input_parameters['final_price']
#               self._teryt = input_parameters['teryt']
#               self._powiat_id = self._teryt[:4]
#               self._area_update_max = 3000
#               self._area_update_min = 300
#               self._brt_tr_ref = []
#               self._similar_tr_df = pd.DataFrame()
# def _download_brt_data(input_parameters: dict):
#        btr_u27_cond1 = """
#                 WHERE
#                 ST_DWithin(ST_Transform(st_setsrid(st_makepoint(:lon,:lat),4326),2180), ST_Transform(st_setsrid(st_makepoint( geo_lon,geo_lat),4326),2180), 20000)
#                     AND data_dokumentu >= :min_reference_date
#                     AND data_dokumentu <= :valuation_date
#                     AND cena_m2 >= :min_price
#                     AND cena_m2 <=  :max_price
#                     AND powiat_id = :powiat_id"""
#
#        btr_u27_cond2 = """
#                 WHERE
#                 ST_DWithin(ST_Transform(st_setsrid(st_makepoint(:lon,:lat),4326),2180), ST_Transform(st_setsrid(st_makepoint( geo_lon,geo_lat),4326),2180), 40000)
#                     AND data_dokumentu >= :min_reference_date
#                     AND data_dokumentu <= :valuation_date
#                     AND cena_m2 >= :min_price
#                     AND cena_m2 <= :max_price
#                     AND powiat_id = :powiat_id"""
#
#        tr_cond_query = """
#                 SELECT CASE WHEN ( SELECT COUNT(*) FROM avm.avm_test_gcb_agl_waw   {statement1} ) >= 30 THEN 1
#                 ELSE 2 END""".format(statement1=btr_u27_cond1)
#
#        base_brt_query = """
#                 SELECT id::text,
#                     powiat_id::text,
#                     teryt::text,
#                     RIGHT(teryt,1)::int rodzaj_gminy,
#                     geo_lat::float,
#                     geo_lon::float,
#
#                     cena_m2::float,
#
#                     to_char(data_dokumentu::timestamp,'YYYY-MM-DD')  transakcja_data_dokumentu,
#                     suma_powierzchni_dzialek::float suma_powierzchni_dzialek,
#                     date_part('year',
#                     age(:valuation_date,data_dokumentu::date))*12 +
#                     date_part('month',age(:valuation_date,data_dokumentu::date)) as month_diff,
#                     ST_Distance(ST_Transform(st_setsrid(st_makepoint( geo_lon,geo_lat),4326),2180), ST_Transform(st_setsrid(st_makepoint( :lon,:lat),4326),2180))::int as distance_m,
#                     ROUND(100 * ABS(1-cena_m2/:final_price), 2)::float as price_percent_diff,
#                     1::int as zgodnosc_filtrow
#                 FROM avm.avm_test_gcb_agl_waw
#     """