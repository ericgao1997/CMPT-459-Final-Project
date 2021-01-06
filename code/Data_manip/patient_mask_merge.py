import pandas as pd 
import os
import sys

def load_statecodes():
    dict = {}
    with open("csv_state_abr.csv",encoding="utf-8") as inFile:
        for line in inFile:
            list = line.replace("\"","").split(",")
            try:
                dict[list[2].strip()] = list[0].strip()
            except:
                print("error")
                print(list)
    return dict

def load_clean_patients():
    dtypes = {
        "date":"category",
        "county":"category",
        "state":"category",
        "fips":"string",
        "cases":"UInt32",
        "deaths":"UInt32"
    }
    county_cases = pd.read_csv(
        "us-counties.csv",
        dtype=dtypes
    )
    county_cases = county_cases.drop(['county','fips'],axis=1)
    county_cases= county_cases.groupby(["date","state"]).agg(['sum'])
    return county_cases

def load_new_patients():
    new_cases = pd.read_pickle("cases_per_day.pkl")
    return new_cases

def modify_mask_opinions(masks_df):
    for index, row in masks_df.iterrows():
        if float(row["Sentiment"]) == 0.0:
            masks_df.loc[index,"Sentiment"] = 0.01
    return masks_df

def load_clean_masks():
    state_codes = load_statecodes()
    dtypes = {
        "Date":"category",
        "Sentiment":"float",
        "City":"category",
        "State":"string"
    }
    city_df = pd.read_csv("cleaned_mask_data.csv", dtype=dtypes)
    
    to_remove = []
    for index, row in city_df.iterrows():
        row["State"] = row["State"].strip()
        if row["State"] == "USA":
            city_df.loc[index,"State"] = row["City"]
        elif len(row["State"]) != 2:
            to_remove.append(index)
        else:
            city_df.loc[index,"State"] = state_codes[row["State"]]
    city_df = city_df.drop(to_remove)
    city_df["State"].astype('category')

    state_masks_df = city_df.drop(["City"],axis=1)
    # state_masks_df = modify_mask_opinions(state_masks_df)
    state_df = state_masks_df.groupby(["Date","State"]).agg(['sum'])
    return state_df
    
def main(argv):
    covid_df = load_new_patients()
    masks_df = load_clean_masks()

    print (covid_df)
    print (masks_df)

    result = pd.concat([covid_df,masks_df],axis = 1, sort=False)
    result = result[result[('Sentiment','sum')].notna()]
    result.columns=['date','state','cases','sentiment']
    print (result)
    result.to_pickle("mask_and_covid.pkl")
    return

if __name__=="__main__":
    main(sys.argv)