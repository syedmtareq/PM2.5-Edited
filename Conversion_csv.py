import pandas as pd

# Define the path to the text file and the output CSV file
txt_file = 'Final_Results_IDW_noQC_Surface_DOY001_v1_mod1.txt'  # Replace with your actual .txt file
csv_file = '2020_Final_9.csv'  # Replace with your desired .csv file

# Read the .txt file
# Adjust 'delimiter' as needed: '\t' for tab, ',' for comma, ' ' for space
df = pd.read_csv(r"C:\Users\smtareq\Desktop\Final_Results_IDW_noQC_Surface_DOY001_v1_mod1.txt")

# Save it as a CSV
df.to_csv(csv_file, index=False)

print(f"Data successfully written to {csv_file}")
