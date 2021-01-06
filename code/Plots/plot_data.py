import os
import sys
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import numpy as np
from scipy.interpolate import CubicSpline

def load_data():
    relevent = pd.read_pickle("mask_and_covid.pkl")
    return relevent

def display_cases_vs_cases(df1,state1,df2,state2):
    ax = plt.gca()
    plt.title(state1+" vs "+state2+" (cases)")
    df1.plot(kind='line',x='date',y = 'cases',ax=ax,color = "tab:blue")
    # ax.tick_params(axis='y',labelcolor="tab:blue")

    df2.plot(kind='line',y = 'cases',ax=ax,color="tab:red")
    ax.set_ylabel('cases_per_day')

    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles,[state1+" new cases",state2+' new cases'])
    plt.gcf().autofmt_xdate()
    
    plt.savefig('state_v_state/'+state1+'_'+state2+'.png')
    plt.show()

def smooth(y,box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def display_cases_vs_sentiment(df,state):
    if os.path.isfile('./state_plots/'+state+'.png'):
        print(state, "picture already generated")
        return

    # Smooth Sentiment
    sent_list = df["sentiment"].to_numpy()
    dates = df['date'].to_numpy()
    smoothedFunc = smooth(sent_list,20)
    print(len(smoothedFunc),len(dates),len(df))
    try:
        sentiment_df = pd.DataFrame({'dates':dates,'sentiment':smoothedFunc},columns=['dates','sentiment'])
    except:
        print ("NOT ENOUGH TWEETS")
        plt.clf()
        return

    ax = plt.gca()
    plt.title(state+" (new covid cases vs. mask sentiment)")
    df.plot(kind='line',x='date',y = 'cases',ax=ax,color = "tab:blue")
    # plt.plot(df['date'],df['cases'],color="tab:blue")
    ax.tick_params(axis='y',labelcolor="tab:blue")

    ax2 = ax.twinx()
    sentiment_df.plot(kind='line',x='dates',y = 'sentiment',ax=ax2,color = "tab:red")

    # Create Legend/Axis labels and colors, along with set table size
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles1.append(handles2[0])
    lables = labels1+labels2
    ax.legend(handles1,lables)
    ax2.tick_params(axis='y',labelcolor="tab:red")
    ax.set_ylabel('new_cases_per_day')
    ax2.set_ylabel('mask sentiment')
    ax2.get_legend().remove()
    fig = plt.gcf()
    fig.set_size_inches(10, 6)

    plt.savefig('state_mask_plots/'+state+'.png')
    plt.clf()
    # plt.show()

def main(argv):
    if len(argv) == 2:
        state = argv[1]
    elif len(argv) > 2:
        state = argv[1]
        state2 = argv[2]
    else:
        state = "null"


    result_df = load_data()
    result_df.columns = ['date','state','cases','sentiment']
    if state == "null":
        states = result_df['state'].unique()
        for i in states:
            state_df =result_df.loc[result_df['state'] == i]
            if state_df.empty:
                continue
            display_cases_vs_sentiment(state_df,i)
        return
        
    state_df =result_df.loc[result_df['state'] == state]
    display_cases_vs_sentiment(state_df,state)

    if len(argv) > 2:
        state2_df =result_df.loc[result_df['state'] == state2]
        display_cases_vs_cases(state_df,state,state2_df,state2)

    return

if __name__ == "__main__":
    main(sys.argv)