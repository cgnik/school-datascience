from ds import log, pd
from ds.fips import fips_states, fips_counties

if __name__ == '__main__':
    food = pd.read_csv('../data/census_december_2019-food-security.csv.gz', compression='gzip')
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
    # HESP1 : has anyone in house needed SNAP

    cols = ['GCTCO', 'GCFIP', 'HETS8OU', 'HETS8O', 'HES8B', 'HETS8CO', 'HESP1']
    out_data = food[cols]
    out_data = out_data.loc[out_data['GCTCO'] > 0]
    out_data = out_data.loc[out_data['GCFIP'] > 0]
    out_data.columns = ['FIPS_COUNTY', 'FIPS_STATE', 'USUAL_FOOD_SPEND', 'TOTAL_FOOD_SPEND_LAST_WEEK', 'FOOD_WOULD_SPEND_MORE', 'FOOD_SPEND_INCREASE_WEEK', 'RECEIVED_SNAP']
    out_data.to_csv('output/food.csv', index=False)