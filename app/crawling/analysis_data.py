import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_DIR = os.path.join(BASE_DIR, '../data')

def plot_avgscore_by_hometown_and_subject(df, dir, filename):
    #plt.style.use('seaborn-v0_8-darkgrid')

    top_5_hometown = df['hometown'].value_counts().head(5).index
    df_top = df[df['hometown'].isin(top_5_hometown)]
    avg_score = df_top.groupby('hometown')[
                                            ['math_score', 'literature_score', 'english_score']
                                            ].mean().reindex(top_5_hometown)
    avg_score.plot(kind='bar', figsize=(10, 6), color=['#3498db', '#1abc9c', '#e67e22'])
    plt.title("Average Scores by Hometown and Subjects")
    plt.ylabel("Average Scores")
    plt.xlabel("Hometown")
    plt.xticks(rotation=0)
    plt.legend(title="Subject", loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    plt.tight_layout()
    plt.savefig(os.path.join(dir, filename))
    plt.show()

def plot_avgscore_and_ages(df, dir, filename):
    # Add column age
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
    today = pd.Timestamp.now().normalize()
    years = today.year - df['date_of_birth'].dt.year
    not_had_birthday = ((today.month < df['date_of_birth'].dt.month) |
                        ((today.month == df['date_of_birth'].dt.month) & (today.day < df['date_of_birth'].dt.day)))
    years = years - not_had_birthday.astype('Int64')

    # where dob was NaT, result will be NaN
    years = years.astype('Int64')

    # filter unrealistic ages
    years = years.where((years >= 0) & (years <= 120))

    df['age'] = years

    df = df.copy()
    df.dropna(subset=['age', 'math_score', 'literature_score', 'english_score'])
    df_age = df.groupby('age', sort=True)[['math_score', 'literature_score', 'english_score']].mean().reset_index()
    
    df_melted = df_age.melt(id_vars='age', var_name='subject', value_name='score')
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_melted, x='age', y='score', hue='subject', markers='o')
    plt.title("Average Scores by Ages")
    plt.xlabel("Age (years)")
    plt.ylabel("Scores")
    plt.grid(alpha=0.3)
    plt.xticks(df_age['age'])
    plt.savefig(os.path.join(dir, filename))
    plt.show()

def plot_correlation_matrix(df, dir, filename):
    corr = df.corr(numeric_only=True)
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, linewidths=0.5)
    plt.title("Correlation Matrix between Scores and other factors")
    plt.savefig(os.path.join(dir, filename))
    plt.show()

def plot_score_box(df, dir, filename):
    ax = df[['math_score', 'literature_score', 'english_score']].plot.box(figsize=(8, 6))
    print("plot score box df data  : \n")
    print(df[['math_score', 'literature_score', 'english_score']])
    ax.set_title("Score Distribution among Students")
    ax.set_ylabel("Score")
    ax.set_xticklabels(["Math Score", "Literature Score", "English Score"])
    ax.grid(axis='y')

    plt.savefig(os.path.join(dir, filename))
    plt.show()

def plot_score_scatter(df, dir, filename):
    ax = df.plot.scatter(x='math_score', y='english_score', alpha=0.5, figsize=(8, 6))
    ax.set_title("Correlation between Math and English Scores")
    ax.set_xlabel("Math Scores")
    ax.set_ylabel("English Scores")
    ax.grid(True)

    plt.savefig(os.path.join(dir, filename))
    plt.show()

def plot_avg_english_by_hometown(df, dir, filename):

    plt.figure()
    avg_scores = df.groupby('hometown', observed=True)['english_score'].mean().sort_values()
    ax = avg_scores.plot(kind='barh',
                         figsize=(12, 8),
                         color='skyblue')
    ax.set_title('Average English Scores by Hometown')
    ax.set_xlabel('English Scores')
    ax.set_ylabel('Hometown')
    ax.grid(axis='x')
    plt.tight_layout()

    plt.savefig(os.path.join(dir, filename))
    plt.show()

def analysis_data(input_filepath):
    img_dir = 'img'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(base_dir, img_dir)
    os.makedirs(img_dir, exist_ok=True)
    try:
        # Read file
        df = pd.read_csv(input_filepath)
        print("--- Data Analysis ---")
        print(df.info())
        print("\nFirst 5 rows of data:")
        print(df.head())

        # Encode Categorical Variables
        df['hometown'] = df['hometown'].astype('category')

        # Create plots
        plot_score_box(df, img_dir, "score_box.png")
        plot_avg_english_by_hometown(df, img_dir, "english_by_hometown.png")
        plot_avgscore_by_hometown_and_subject(df, img_dir, "avg_by_hns.png")
        plot_correlation_matrix(df, img_dir, "c_matrix.png")
        plot_avgscore_and_ages(df, img_dir, "avgs_and_ages.png")
        plot_score_scatter(df, img_dir, "scatter_math_english.png")
        

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    # It is recommended to run main.py
    # This is for running the script directly from the 'analysis' directory
    # analysis_data("cleaned_student_data.csv")
    input_path = os.path.join(CSV_DIR, "students_data.csv")
    analysis_data(input_path)
