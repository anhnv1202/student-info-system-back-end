# import pandas as pd

# def clean_student_data(input_filepath, output_filepath):

#     try:
#         # Read file / inspect dataprint / print first 5 rows
#         df = pd.read_csv(input_filepath)
#         print("--- Data Before Cleaning ---")
#         print(df.info())
#         print("\nFirst 5 rows of original data:")
#         print(df.head())

#         # Drop column with too many NaNs(> 50% data is NaN)
#         columns_to_drop = df.columns[df.isnull().mean() > 0.5]
#         if not columns_to_drop.empty:
#             print("\nColumns to drop:" + str(columns_to_drop))
#         df.drop(columns=columns_to_drop, inplace=True)

#         # Clean string columns by stripping leading/trailing whitespace
#         for col in df.select_dtypes(include=['object']).columns:
#             df[col] = df[col].str.strip()

#         # Rename all columns
#         df.rename(columns={'Mã số sinh viên': 'student_code',
#                            'Họ': 'first_name',
#                            'Tên': 'last_name',
#                            'Email': 'email',
#                            'Ngày sinh': 'date_of_birth',
#                            'Quê quán': 'hometown',
#                            'Điểm Toán': 'math_score',
#                            'Điểm Văn': 'literature_score',
#                            'Điểm Tiếng Anh': 'english_score'
#                            }, inplace=True)

#         # Clean score columns
#         score_columns = ['math_score', 'literature_score', 'english_score']
#         for col in score_columns:
#             # convert column to numeric, coercing errors into NaN
#             df[col] = pd.to_numeric(df[col], errors='coerce')

#             # Convert value not in [0, 10] to NaN
#             valid_number_condition = df[col].between(0, 10)
#             df[col] = df[col].where(valid_number_condition)

#             #  Remove row if all scores is NaN
#             df.dropna(subset=score_columns, how='all', inplace=True)

#             # Fill missing values (NaN) with the mean of the column
#             # mean_score = df[col].mean()
#             # df[col].fillna(mean_score, inplace=True)

#             df[col] = df[col].round(2)

#         # Adding new Features: Fullname & Avg_Score
#         df.insert(1, 'full_name', df['first_name'] + ' ' + df['last_name'])
#         df.drop(columns=['first_name', 'last_name'], inplace=True)

#         # df['avg_score'] = df[score_columns].mean(axis=1)
#         # df['avg_score'] = df['avg_score'].round(2)

#         print("\n--- Data After Cleaning ---")
#         print(df.info())
#         print("\nFirst 5 rows of cleaned data:")
#         print(df.head())

#         #  Save to a new CSV file
#         df.to_csv(output_filepath, index=False, encoding='utf-8-sig')

#         print(f"\n✅ Data cleaning complete. Cleaned file saved to '{output_filepath}'")

#     except FileNotFoundError:
#         print(f"Error: The file '{input_filepath}' was not found.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")


# if __name__ == '__main__':
#     clean_student_data("danh_sach_sinh_vien.csv", "cleaned_student_data.csv")

import pandas as pd
from datetime import datetime

def clean_student_data(input_filepath, output_filepath):
    try:
        df = pd.read_csv(input_filepath)
        print("--- Data Before Cleaning ---")
        print(df.info())
        print("\nFirst 5 rows of original data:")
        print(df.head())

        # Drop any column >50% missing
        columns_to_drop = df.columns[df.isnull().mean() > 0.5]
        if not columns_to_drop.empty:
            print("\nColumns to drop:" + str(columns_to_drop))
        df.drop(columns=columns_to_drop, inplace=True)

        # Strip whitespace for all string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()

        # === Clean date_of_birth ===
        def parse_date(x):
            try:
                return pd.to_datetime(x, errors='coerce', dayfirst=True)
            except:
                return pd.NaT
        df['date_of_birth'] = df['date_of_birth'].apply(parse_date)

        # === Clean scores ===
        score_columns = ['math_score', 'literature_score', 'english_score']
        for col in score_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].where(df[col].between(0, 10))

        # Drop rows with all scores invalid
        df.dropna(subset=score_columns, how='all', inplace=True)

        # === Clean email ===
        def valid_email(email):
            if not isinstance(email, str): return None
            return email if "@" in email and "." in email else None
        df['email'] = df['email'].apply(valid_email)

        # === Add full_name & average score ===
        df['full_name'] = df['first_name'].fillna('') + ' ' + df['last_name'].fillna('')
        df['avg_score'] = df[score_columns].mean(axis=1).round(2)

        # Reorder columns
        df = df[['student_code', 'full_name', 'email', 'date_of_birth', 'hometown',
                 'math_score', 'literature_score', 'english_score', 'avg_score']]

        print("\n--- Data After Cleaning ---")
        print(df.info())
        print("\nFirst 5 rows of cleaned data:")
        print(df.head())

        df.to_csv(output_filepath, index=False, encoding='utf-8-sig')
        print(f"\n✅ Cleaned file saved to '{output_filepath}'")

    except FileNotFoundError:
        print(f"Error: The file '{input_filepath}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
