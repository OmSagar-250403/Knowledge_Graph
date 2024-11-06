import csv
import os

# Use with statement to open and read the CSV file with specified encoding
with open('assets/final_dataset_imdb.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        print(row)  # Print each row