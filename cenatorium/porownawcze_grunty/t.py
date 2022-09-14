from LandXKNMain import BuildingLAndXKN
import numpy as np


class BuildingLandReferenceTransaction(LandXKNMain):

    def __init__(self, con, input_parameters):
        super().__init__(con, input_parameters)

        self._search_brt_db_params = {
            'lon': self._geo_lon,
            'lat': self._geo_lat,
            'powiat_id': self._powiat_id,
            'valuation_date': self._valuation_date,
            'final_price': self._final_price,
            'min_reference_date': self._min_reference_date,
            'max_price': self._final_price * (1 + self._max_percent_price / 100),
            'min_price': self._final_price * (1 - self._max_percent_price / 100),
            'area_min': self._area * 0.5,
            'area_max': self._area * 2.5}


    def _download_brt_data(self):
        tr_query = """
                        SELECT  COUNT(*) FROM avm.avm_test_gcb_agl_waw    WHERE
                            ST_DWithin(ST_Transform(st_setsrid(st_makepoint(:lon,:lat),4326),2180), ST_Transform(st_setsrid(st_makepoint( geo_lon,geo_lat),4326),2180), 20000)
    
                                AND data_dokumentu <= :valuation_date 
                                AND cena_m2 >= :min_price
                                AND cena_m2 <=  :max_price
                                AND powiat_id = :powiat_id 
                         """

        self._selected_query = input_similar_tr_df_count(
            query_sql=tr_query,
            input_parameters=search)

    def _download_unclean_brt_data(self):
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

        self.similar_tr_df = get_similar_database_from_sql(
            query_sql=brt_u27_unclean_query,
            input_parameters=search)


    def update_price_cost(self):
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