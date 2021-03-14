EMAT-64210 Data Science project and class work
==================================

The [ds.churn](ds/churn/__init__.py) package is exploratory, in nature, and relies on the MegaTelCo [churn arff dataset from weka](https://learn.kent.edu/bbcswebdav/pid-12975843-dt-content-rid-169449187_1/xid-169449187_1), and most exploration (though in python) was intended to parallel Weka class exercises and exploration.

[Food insecurity data](https://www2.census.gov/programs-surveys/cps/datasets/2019/supp/dec19pub.csv) and [technical documentation](https://www2.census.gov/programs-surveys/cps/techdocs/cpsdec19.pdf) can be downloaded from [here](https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-food-security.html#cpssupps).

The [Farm Survey](https://www.nass.usda.gov/Publications/AgCensus/2017/Online_Resources/Census_Data_Query_Tool/2017_cdqt_data.txt.gz) and associated [usage application](https://www.nass.usda.gov/Quick_Stats/CDQT/chapter/1/table/1) is available in tab-separated .txt file from [here](https://www.nass.usda.gov/AgCensus/).

In this repository, FIPS county codes are used to cross-reference the geographic co-location of the farms and the food insecurity data.  The FIPS State and County codes were taken from tables at the end of the [Food Insecurity technical documentation](https://www2.census.gov/programs-surveys/cps/techdocs/cpsdec19.pdf). The code which was used to process that data is found in the [ds.fips](ds/fips/__init__.py) package.

Data files used for the project were output to the [output](output/)