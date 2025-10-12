from clean_data import clean_student_data
from analysis_data import analysis_data

def main():
    input_csv = "danh_sach_sinh_vien.csv"
    cleaned_csv = "cleaned_student_data.csv"

    print("--- Starting Data Cleaning ---")
    clean_student_data(input_csv, cleaned_csv)
    print("\n--- Data Cleaning Finished ---")

    print("\n--- Starting Data Analysis ---")
    analysis_data(cleaned_csv)
    print("\n--- Data Analysis Finished ---")

if __name__ == '__main__':
    main()
