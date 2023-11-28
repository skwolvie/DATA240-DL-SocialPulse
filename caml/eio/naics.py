import pandas as pd
useeio_file = "https://pasteur.epa.gov/uploads/10.23719/1528686/SupplyChainGHGEmissionFactors_v1.2_NAICS_CO2e_USD2021.csv"
naics_file = "https://www.census.gov/naics/2017NAICS/2017_NAICS_Index_File.xlsx"

def get_naics_data():
    useeio_df = pd.read_csv(useeio_file)
    useeio_df = useeio_df[['2017 NAICS Code', '2017 NAICS Title', 'Supply Chain Emission Factors with Margins', 'Reference USEEIO Code']]
    useeio_df = useeio_df.rename(columns={
        "2017 NAICS Code": "naics_code",
        "2017 NAICS Title": "naics_title",
        "Supply Chain Emission Factors with Margins": "co2e_per_dollar",
        "Reference USEEIO Code": "bea_code",
    })
    print(useeio_df.shape)
    useeio_df.head()

    naics_df = pd.read_excel(naics_file)
    naics_df = naics_df.rename(columns={
        "NAICS17": "naics_code",
        "INDEX ITEM DESCRIPTION": "naics_desc",
    })
    print(naics_df.shape)
    naics_df = pd.merge(naics_df, useeio_df, on="naics_code", how="left").dropna()
    naics_df = naics_df.groupby('naics_desc').first().reset_index()
    return naics_df
