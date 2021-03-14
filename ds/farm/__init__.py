from ds import log, pd

if __name__ == '__main__':
    # the following file available from https://www.nass.usda.gov/AgCensus/
    # https://www.nass.usda.gov/Publications/AgCensus/2017/Online_Resources/Census_Data_Query_Tool/2017_cdqt_data.txt.gz
    farms = pd.read_csv('../data/2017_cdqt_data.txt.gz', compression='gzip', sep='\t')
    log.info(f"FARMS: {farms}")
    log.info(f"FARMS COLUMNS: {farms.columns}")
