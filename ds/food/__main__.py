from ds import log, pd
from ds.fips import fips_states, fips_counties
import csv

if __name__ == '__main__':
    food = pd.read_csv('../data/census_december_2019-food-security.csv.gz', compression='gzip',
                       dtype={'GCTCO': object, 'GCFIP': object})
    log.info(f"FOOD: {food}")
    log.info(f"FOOD COLUMNS: {food.columns}")
    cols = lambda c, s: [(i, k) for i, k in enumerate(c) if k.startswith(s)]
    for l in ['HET', 'GCT']: print(f"COLS ({l}): {cols(food.columns, l)}")
    log.info(f"GCTCO? {list(food['GCTCO'].unique())}")
    log.info(f"GCTFIP? {list(food['GCFIP'].unique())}")
    # GCTCO : FIPS county code
    # GCFIP : FIPS state code
    # HETS8OU : Usual amount spent on food per week
    # HETS80 : total amount spent on food last week
    # HES8B : would you spend more(1), less(2), same(3) to meet weekly food needs of household
    # HETS8CO : how much more per week to meet food needs of household: - indicates not respond
    # HESP1 : has anyone in house needed SNAP yes(1) no(2)
    # HESS4 : couldn't afford balanced meals: often(3) sometimes(2) never(1)

    cols = ['GCTCO', 'GCFIP', 'HETS8OU', 'HETS8O', 'HES8B', 'HETS8CO', 'HESP1', 'HESS4']
    out_data = food[cols]
    out_data.columns = ['FIPS_COUNTY', 'FIPS_STATE', 'USUAL_FOOD_SPEND', 'TOTAL_FOOD_SPEND_LAST_WEEK',
                        'FOOD_NEED_MORE', 'FOOD_SPEND_INCREASE_WEEK', 'RECEIVED_SNAP', 'NOT_AFFORD_BALANCED_MEALS']
    out_data = out_data.loc[((out_data['FIPS_COUNTY'].notna()) & (out_data['FIPS_STATE'].notna()))]
    print(f"OUTPUTTING food data: len {len(out_data)}")
    out_data.to_csv('output/food.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
