import pandas as pd

from datetime import datetime

tokyo_debut_date = datetime(2021, 8, 8)
paris_debut_date = datetime(2024, 7, 26) 

olympic_data_1 =  pd.read_csv("./data/olympic_data_1896_2016/athlete_events.csv")
olympic_data_1.rename(columns= {'Event' : 'complete_event', 'Name' : 'name', 'Sex': 'sex', 'Age' : 'age', 'Height' : 'height',
                                 'Team' : 'team' , 'Year' : 'year', 'Season': 'season', 'City': 'city', 'Medal' :'medal' }, inplace= True)
# print(olympic_data_1.columns)
# print(olympic_data_1.head(5))
olympic_athletes_2 =  pd.read_csv("./data/olympic_data_2020/athletes.csv")
# print(olympic_athletes_2.columns)
olympic_athletes_2["year"] = 2020
olympic_athletes_2["season"] = "Summer"
olympic_athletes_2["city"] = "Tokyo" 
olympic_athletes_2["sex"] = olympic_athletes_2["gender"].map({"Male" :'M', "Female": 'F'})

olympic_athletes_2["height_in_meters"] = olympic_athletes_2["height_m/ft"].str.split("/").str[0]
# Converting the extracted values to float
olympic_athletes_2['height_in_meters'] = olympic_athletes_2['height_in_meters'].astype(float)
olympic_athletes_2['height'] = olympic_athletes_2["height_in_meters"]*100

olympic_athletes_2.rename(columns={'discipline': 'complete_event', 'country' : "team"}, inplace=True)

olympic_athletes_2["birth_date"] = pd.to_datetime(olympic_athletes_2['birth_date']) 

# Function to calculate age
def calculate_age(birth_date, reference_date):
    return reference_date.year - birth_date.year - ((reference_date.month, reference_date.day) < (birth_date.month, birth_date.day))

# Apply the age calculation to each row
olympic_athletes_2['age'] = olympic_athletes_2['birth_date'].apply(lambda x: calculate_age(x, tokyo_debut_date))

# print(olympic_athletes_2.columns)
# print(olympic_athletes_2.head())

athletes_columns = ["name", "sex", "age", "height","team","year","season","city","complete_event"]
medals_columns = ["athlete_name", "athlete_sex", "year", "season", "country", "complete_event", "medal"]
total_medals_columns = ["country", "year", "season","gold_medal", "silver_medal", "bronze_medal","total"]

olympic_athletes = pd.concat([olympic_data_1[athletes_columns], olympic_athletes_2[athletes_columns]])

olympic_athletes_3 =  pd.read_csv("./data/olympic_data_2024/athletes.csv")
# print(olympic_athletes_3.columns)
# print(olympic_athletes_3["events"])
# print(olympic_athletes_3["events"].value_counts())

olympic_athletes_3["year"] = 2024
olympic_athletes_3["season"] = "Summer"
olympic_athletes_3["city"] = "Paris" 
olympic_athletes_3["sex"] = olympic_athletes_3["gender"].map({"Male" :'M', "Female": 'F'})

olympic_athletes_3.rename(columns={'country' : "team" }, inplace=True)

olympic_athletes_3["complete_event"] = olympic_athletes_3["events"] + olympic_athletes_3["disciplines"]
olympic_athletes_3["birth_date"] = pd.to_datetime(olympic_athletes_3['birth_date']) 


# Apply the age calculation to each row
olympic_athletes_3['age'] = olympic_athletes_3['birth_date'].apply(lambda x: calculate_age(x, paris_debut_date))
olympic_athletes = pd.concat([olympic_athletes, olympic_athletes_3[athletes_columns]])

# display the data of olympiuc athletes
# print(olympic_athletes)
olympic_athletes.to_csv("./data/results/athletes.csv")

#preparing the dataset of medals

olympic_medals_subset = olympic_data_1[["name","sex","year","season","team","complete_event","medal"]] 
olympic_medals = olympic_medals_subset.dropna(subset="medal")

olympic_medals.rename(columns={'name': 'athlete_name', 'sex' : 'athlete_sex', 'team' : 'country' }, inplace=True)
# print(olympic_medals.head())

tokyo_medals = pd.read_csv("./data/olympic_data_2020/medals.csv")

tokyo_medals["complete_event"] =tokyo_medals["event"] + tokyo_medals["discipline"]
tokyo_medals["year"] = 2020
tokyo_medals["season"] = "Summer"
# tokyo_medals["medal"] = tokyo_medals["medal_type"].map(lambda x:  x.split()[0])
# Define a mapping dictionary for the medal codes
medal_mapping = {1: 'Gold', 2: 'Silver', 3: 'Bronze'}
# Use the map function to create a new 'medal' column
tokyo_medals["medal"] = tokyo_medals["medal_code"].map(medal_mapping)

# # Print to check the result
# print(tokyo_medals.head())

# print(tokyo_medals[tokyo_medals["country_code"]=="USA"]["medal"])
# # print(tokyo_medals.head())


olympic_medals = pd.concat([olympic_medals[medals_columns], tokyo_medals[medals_columns]])

paris_medals = pd.read_csv("./data/olympic_data_2024/medals.csv")
paris_medals.rename(columns={'name': 'athlete_name', 'gender' : 'athlete_sex'}, inplace=True)
paris_medals["complete_event"] =paris_medals["event"] + paris_medals["discipline"]
paris_medals["year"] = 2024
paris_medals["medal"] = paris_medals["medal_type"].map(lambda x:  x.split()[0])
paris_medals["season"] = "Summer"
# print(paris_medals.head())

olympic_medals = pd.concat([olympic_medals[medals_columns], paris_medals[medals_columns]])
olympic_medals["year"].astype(int)

olympic_medals.to_csv("./data/results/olympic_medals.csv")

# Now drop duplicates based on 'complete_event'
olympic_medals_unique = olympic_medals.drop_duplicates(subset=["complete_event", "country", "medal"])


# Selecting specific columns from the DataFrame
total_medals = olympic_medals_unique.loc[:, ["country", "year", "season", "medal"]]

# Display the updated DataFrame
# print(total_medals.head())

# Create a pivot table to count each medal type for each country
medal_count = total_medals.pivot_table(index=['country', 'year', "season"], columns='medal', aggfunc='size', fill_value=0)
# print(medal_count)

# Renaming columns to make it clearer
medal_count = medal_count.rename(columns={
    'Gold': 'gold_medal',
    'Silver': 'silver_medal',
    'Bronze': 'bronze_medal'
})

# Calculating the total number of medals for each country
medal_count['total_medals'] = medal_count.sum(axis=1)

# Reset index to make 'Country' a column again
medal_count = medal_count.reset_index()
# print(medal_count.head(10))

# print(medal_count[medal_count["season"] == "Winter"])

# Define the desired column order
desired_column_order = ["country", "year", "season", "gold_medal", "silver_medal", "bronze_medal", "total_medals"]

# Reorder the columns
medal_count = medal_count[desired_column_order]

# # Now display the medal count of Morocco for the year 2020 in the desired order, sorted by Gold Medal
# print(medal_count[medal_count["year"] == 2020].sort_values(by=['Gold Medal', 'Silver Medal', 'Bronze Medal'], ascending=False).head(20))

medal_count.to_csv("./data/results/medals.csv")
