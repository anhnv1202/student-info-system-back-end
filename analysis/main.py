from clean_data import clean_student_data
from analysis_data import analysis_data
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_DIR = os.path.join(BASE_DIR, 'csvdata')

def main():
    input_csv = os.path.join(CSV_DIR, "sample_data.csv")
    cleaned_csv = os.path.join(CSV_DIR, "cleaned_data.csv")

    print("--- Starting Data Cleaning ---")
    clean_student_data(input_csv, cleaned_csv)
    print("\n--- Data Cleaning Finished ---")

    print("\n--- Starting Data Analysis ---")
    analysis_data(cleaned_csv)
    print("\n--- Data Analysis Finished ---")

if __name__ == '__main__':
    main()
