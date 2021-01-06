To Run the project: 

1. Start by hydrating the tweets by running the command:
C:/<path to "tweet" folder>python cleaned_tweet_pull.py

2. Run the tweet analyzer and roll up program called "tweetReadClean.py"
C:/<path to "tweet" folder>python tweetReadClean.py

3. This should output a "cleaned_mask_data.csv" file, which needs to be moved to the "Data_manip" folder.
4. Here, we run the "state_cleanup.py" program to read in the county/state cases file, and roll them up along with transforming them into per-day statistics
C:/<path to "Data_manip">python state_cleanup.py

5. This should result in a "cases_per_day.pkl" file which contains the state case data. Next we run "patient_mask_merge.py" to append the two datasets together
C:/<path to "Data_manip">python patient_mask_merge.py

6. This should output the "mask_and_covid.pkl" file, which contains the final merged dataset. 
	This file should be moved to the "Plots" folder for final visualization.

7. In the plots folder is the program "plot_data.py". There are 3 ways to run this program

-Options-
C:/<path to "Plots">python plot_data.py 
	-- Will run the plotting program and produce a "sentiment vs. cases" image in the "state_mask_plots" folder for EVERY state.

C:/<path to "Plots">python plot_data.py "<State Name>"
	-- Will run the plotting program and produce a "sentiment vs. cases" image in the "state_mask_plots" folder for "<State Name>".

C:/<path to "Plots">python plot_data.py "<State Name>" "<State Name 2>"
	-- Will plot a comparison plot of the cases in "<State Name>" and "<State Name 2>", saves into "state_v_state"