from ds import log, pd

states = [(6, 'CA'), (45, 'SC'), (23, 'ME'), (38, 'ND'), (22, 'LA'), (8, 'CO'), (24, 'MD'), (28, 'MS'), (46, 'SD'),
          (25, 'MA'), (13, 'GA'), (2, 'AK'), (37, 'NC'), (54, 'WV'), (56, 'WY'), (11, 'DC'), (1, 'AL'), (19, 'IA'),
          (39, 'OH'), (47, 'TN'), (30, 'MT'), (32, 'NV'), (34, 'NJ'), (4, 'AZ'), (9, 'CT'), (36, 'NY'), (50, 'VT'),
          (53, 'WA'), (31, 'NE'), (29, 'MO'), (40, 'OK'), (27, 'MN'), (16, 'ID'), (35, 'NM'), (41, 'OR'), (26, 'MI'),
          (5, 'AR'), (17, 'IL'), (10, 'DE'), (49, 'UT'), (48, 'TX'), (44, 'RI'), (33, 'NH'), (12, 'FL'), (20, 'KS'),
          (21, 'KY'), (55, 'WI'), (42, 'PA'), (18, 'IN'), (51, 'VA'), (15, 'HI')]
counties = []



# if __name__ == '__main__':
#     food = pd.read_csv('../data/census_december_2019-food-security.csv.gz', compression='gzip')
#     log.info(f"FOOD: {food}")
#     log.info(f"FOOD COLUMNS: {food.columns}")
#     log.info(f"FOOD COLUMNS: {[(i, c) for i, c in enumerate(food.columns) if c.startswith('G')]}")
#     log.info(f"FOOD COLUMNS: {[c for c in food.columns if 'FIPS' in c]}")
#     log.info(f"GCTCO? {list(food['GCTCO'].unique())}")
#     log.info(f"GCTFIP? {list(food['GCFIP'].unique())}")
#     state_lookups = [next(filter(lambda x: x[0] == s, states)) for s in food['GCFIP'].unique()]
#     log.info(f"state lookups: {state_lookups}")


fips_states_from_pdf = """
01 AL 30 MT
02 AK 31 NE
04 AZ 32 NV
05 AR 33 NH
06 CA 34 NJ
08 CO 35 NM
09 CT 36 NY
10 DE 37 NC
11 DC 38 ND
12 FL 39 OH
13 GA 40 OK
15 HI 41 OR
16 ID 42 PA
17 IL 44 RI
18 IN 45 SC
19 IA 46 SD
20 KS 47 TN
21 KY 48 TX
22 LA 49 UT
23 ME 50 VT
24 MD 51 VA
25 MA 53 WA
26 MI 54 WV
27 MN 55 WI
28 MS 56 WY
29 MO"""
fips_states = re.split('(\d\d) (\w\w)[\n\r ].', fips_states_from_pdf)
counties_from_pdf = """
FIPS
County County
Code Name State
Alabama
003 Baldwin*
015 Calhoun
073 Jefferson
097 Mobile
117 Shelby
Arizona
003 Cochise*
013 Maricopa
015 Mohave*
019 Pima
021 Pinal
025 Yavapai
Arkansas
119 Pulaski
California
001 Alameda
007 Butte
017 El Dorado
019 Fresno
025 Imperial
029 Kern
037 Los Angeles
039 Madera
047 Merced
053 Monterey
055 Napa
059 Orange
061 Placer
067 Sacramento
071 San Bernardino
073 San Diego
075 San Francisco
077 San Joaquin
FIPS
County County
Code Name State
11-16
079 San Luis Obispo
081 San Mateo
083 Santa Barbara
087 Santa Cruz
095 Solano
097 Sonoma
099 Stanislaus
107 Tulare
111 Ventura
113 Yolo
Colorado
013 Boulder
031 Denver
035 Douglas
059 Jefferson
069 Larimer
101 Pueblo
123 Weld
Delaware
001 Kent
003 New Castle
005 Sussex*
District of Columbia
001 District of Columbia
Florida
001 Alachua
005 Bay
009 Brevard
011 Broward
015 Charlotte
019 Clay
021 Collier
053 Hernando
057 Hillsborough
061 Indian River
069 Lake
071 Lee
083 Marion
086 Miami-Dade
091 Okaloosa
095 Orange
FIPS
County County
Code Name State
11-17
097 Osceola
099 Palm Beach
101 Pasco
103 Pinellas
105 Polk
109 St. Johns
117 Seminole
127 Volusia
Georgia
057 Cherokee
063 Clayton
135 Gwinnett
151 Henry
153 Houston
Hawaii
001 Hawaii*
003 Honolulu
Idaho
055 Kootenai
Illinois
091 Kankakee
099 LaSalle
111 McHenry
113 McLean
115 Macon
119 Madison
163 St. Clair
179 Tazewell
Indiana
057 Hamilton
063 Hendricks
081 Johnson
089 Lake
091 LaPorte
095 Madison
141 St. Joseph
FIPS
County County
Code Name State
11-18
Iowa
103 Johnson
113 Linn
153 Polk
163 Scott
Kansas
045 Douglas
173 Sedgwick
Kentucky
067 Fayette
111 Jefferson
117 Kenton
Louisiana
019 Calcasieu
033 East Baton Rouge
051 Jefferson
071 Orleans
103 St. Tammany
Maine
011 Kennebec
Maryland
003 Anne Arundel
013 Carroll
017 Charles
025 Harford
027 Howard
033 Prince Georges
043 Washington
FIPS
County County
Code Name State
11-19
Michigan
005 Allegan*
021 Berrien
049 Genesee
075 Jackson
081 Kent
099 Macomb
115 Monroe
121 Muskegon
125 Oakland
139 Ottawa
145 Saginaw
147 St. Clair
161 Washtenaw
163 Wayne
Minnesota
003 Anoka
037 Dakota
123 Ramsey
137 St. Louis
163 Washington
Missouri
019 Boone
099 Jefferson
189 St. Louis
Montana
111 Yellowstone
Nebraska
153 Sarpy
Nevada
003 Clark
FIPS
County County
Code Name State
11-20
New Jersey
001 Atlantic
003 Bergen
005 Burlington
007 Camden
011 Cumberland
013 Essex
017 Hudson
019 Hunterdon
021 Mercer
025 Monmouth
027 Morris
029 Ocean
035 Somerset
037 Sussex
041 Warren
New Mexico
001 Bernalillo
013 Dona Ana
045 San Juan
049 Santa Fe
New York
005 Bronx
013 Chautauqua*
027 Dutchess
047 Kings
055 Monroe
059 Nassau
061 New York
067 Onondaga
069 Ontario
071 Orange
081 Queens
085 Richmond
103 Suffolk
111 Ulster
119 Westchester
FIPS
County County
Code Name State
11-21
North Carolina
057 Davidson*
067 Forsyth
097 Iredell*
119 Mecklenburg
133 Onslow
155 Robeson*
179 Union
183 Wake
North Dakota
017 Cass
Ohio
023 Clark
025 Clermont
029 Columbiana*
035 Cuyahoga
041 Delaware
045 Fairfield
049 Franklin
089 Licking
095 Lucas
103 Medina
133 Portage
153 Summit
165 Warren
169 Wayne*
Oklahoma
031 Comanche
Oregon
017 Deschutes
029 Jackson
039 Lane
043 Linn* 
FIPS
County County
Code Name State
11-22
Pennsylvania
003 Allegheny
007 Beaver
013 Blair
011 Berks
017 Bucks
019 Butler
021 Cambria
029 Chester
045 Delaware
049 Erie
055 Franklin*
071 Lancaster
089 Monroe*
091 Montgomery
101 Philadelphia
125 Washington
129 Westmoreland
133 York
South Carolina
007 Anderson
045 Greenville
051 Horry
063 Lexington
079 Richland
083 Spartanburg
Tennessee
093 Knox
165 Sumner
187 Williamson
FIPS
County County
Code Name State
11-23
Texas
029 Bexar
039 Brazoria
139 Ellis
141 El Paso
183 Gregg
215 Hidago
251 Johnson
303 Lubbock
309 McLennan
329 Midland
439 Tarrant
479 Webb
Utah
049 Utah

Virginia
013 Arlington
041 Chesterfield
059 Fairfax
087 Henrico
107 Loudoun
153 Prince William
510 Alexandria City
550 Chesapeake City
650 Hampton City
700 Newport News City
710 Norfolk City
740 Portsmouth City
760 Richmond City
810 Virginia Beach City
Washington
033 King
035 Kitsap
063 Spokane
067 Thurston
073 Whatcom
077 Yakima
FIPS
County County
Code Name State
11-24
Wisconsin
063 La Crosse
073 Marathon
101 Racine
105 Rock
139 Winnebago"""