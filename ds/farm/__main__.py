from ds import log, pd

if __name__ == '__main__':
    # the following file available from https://www.nass.usda.gov/AgCensus/
    # https://www.nass.usda.gov/Publications/AgCensus/2017/Online_Resources/Census_Data_Query_Tool/2017_cdqt_data.txt.gz
    farms = pd.read_csv('../data/2017_cdqt_data.txt.gz', compression='gzip', sep='\t')
    farms_count = len(farms)
    farm_feature_count = len(farms.columns)
    log.info(f"FARMS: {farms}")
    log.info(f"FARMS COLUMNS: {farms.columns}")
    """ FARMS COLUMNS: Index(['CENSUS_CHAPTER', 'CENSUS_TABLE', 'CENSUS_ROW', 'CENSUS_COLUMN', 'SECTOR_DESC', 'SHORT_DESC', 
    'COMMODITY_DESC', 'AGG_LEVEL_DESC', 'STATE_FIPS_CODE', 'STATE_ALPHA', 'STATE_NAME', 'COUNTY_CODE', 'COUNTY_NAME', 
    'DOMAINCAT_DESC', 'VALUE'], dtype='object')
    
    COMMODITY_DESC gives a good specific set of actual products we could subselect
    
    """
    farms = farms.loc[farms['AGG_LEVEL_DESC'] == 'COUNTY']
    farms = farms.loc[farms['SECTOR_DESC'] == 'CROPS']
    farms = farms.loc[farms['COUNTY_CODE'].notna()]
    farms = farms.loc[farms['STATE_FIPS_CODE'].notna()]
    farms['COUNTY_CODE'] = farms['COUNTY_CODE'].apply(lambda c: int(c))
    cols = ['STATE_FIPS_CODE',  'COUNTY_CODE', 'COUNTY_NAME', 'SECTOR_DESC', 'COMMODITY_DESC']
    farms = farms[cols]
    print(f"FARM data: processed {farms_count} records, {farm_feature_count} features\nRESULTS: {len(farms)} records, {len(farms.columns)} features")
    out_data = farms
    out_data.to_csv('output/farms.csv', index=False)