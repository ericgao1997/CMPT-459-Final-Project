import pandas as pd 
import os
import sys

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

def convert_to_newcases(old_df):
    old_dict = {}
    for index,row in old_df.iterrows():
        if row["state"] not in old_dict.keys():
            old_dict[row["state"]] = row[("cases","sum")]
            continue
        else:
            diff = int(row[("cases","sum")]) - int(old_dict[row["state"]])
            old_dict[row["state"]] = row[("cases","sum")]
            old_df.loc[index,("cases","sum")] = diff
    return old_df

def main(argv):
    state_cases_df = load_clean_patients()
    print (state_cases_df)
    mp_df = state_cases_df.index.to_frame(name=["date","state"])
    result_df = pd.concat([mp_df,state_cases_df],axis = 1, sort=False)
    result_df = result_df[result_df[("cases","sum")].notna()]
    state_per_day = convert_to_newcases(result_df)
    print (state_cases_df)
    state_per_day = state_per_day.drop([("deaths","sum")],axis=1)
    print (state_per_day)
    state_per_day.to_pickle("cases_per_day.pkl")
    return

if __name__=="__main__":
    main(sys.argv)