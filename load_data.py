import pandas as pd

#Loading the dataset
file_path = "data/creditcard.csv"
df = pd.read_csv(file_path)

#Displaying basic info
print(df.info())
print(df.describe())

#Checking for missing values
print(df.isnull().sum())

#Saving the cleaned data
df.to_csv("data/cleaned_creditcard.csv", index=False)
print("✅ Data saved after preprocessing!")
