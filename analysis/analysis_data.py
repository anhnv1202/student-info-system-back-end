import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_score_box(df, dir, filename):
    ax = df[['math_score', 'literature_score', 'english_score']].plot.box(figsize=(8, 6))
    ax.set_title("Phân phối điểm của sinh viên")
    ax.set_ylabel("Điểm")
    ax.set_xticklabels(["Điểm Toán", "Điểm Văn", "Điểm Tiếng Anh"])
    ax.grid(axis='y')

    plt.savefig(os.path.join(dir, filename))
    plt.show()

def plot_score_scatter(df, dir, filename):
    ax = df.plot.scatter(x='math_score', y='english_score', alpha=0.5, figsize=(8, 6))
    ax.set_title("Tương quan điểm Toán và Tiếng Anh")
    ax.set_xlabel("Điểm Toán")
    ax.set_ylabel("Điểm Tiếng Anh")
    ax.grid(True)

    plt.savefig(os.path.join(dir, filename))
    plt.show()

def plot_score_area(df, dir, filename):
    score_columns = ['math_score', 'literature_score', 'english_score']
    new_labels = ["Điểm Toán", "Điểm Văn", "Điểm Tiếng Anh"]
    axs = df[score_columns].plot.area(figsize=(10, 4), subplots=True)
    plt.suptitle("Phân phối điểm của sinh viên (Biểu đồ diện tích)")
    for i, ax in enumerate(axs):
        handles, _ = ax.get_legend_handles_labels()
        ax.legend(handles, [new_labels[i]], bbox_to_anchor=(1, 0.7))
    plt.tight_layout()

    plt.savefig(os.path.join(dir, filename))
    plt.show()

def plot_avg_english_by_hometown(df, dir, filename):

    plt.figure()
    avg_scores = df.groupby('hometown', observed=True)['english_score'].mean().sort_values()
    ax = avg_scores.plot(kind='barh',
                         figsize=(12, 8),
                         color='skyblue')
    ax.set_title('Điểm Tiếng Anh Trung Bình theo Quê Quán')
    ax.set_xlabel('Điểm Trung Bình Tiếng Anh')
    ax.set_ylabel('Quê Quán')
    ax.grid(axis='x')
    plt.tight_layout()

    plt.savefig(os.path.join(dir, filename))
    plt.show()

def plot_math_score_distribution(df, column_name, show_name, dir, filename):
    bins = range(0, 11)
    labels = [f'{i}-{i+1}' for i in range(0, 10)]
    df['temp_column'] = pd.cut(df[column_name], bins=bins, labels=labels, right=False, include_lowest=True)

    score_counts = df['temp_column'].value_counts().sort_index()
    ax = score_counts.plot(kind='bar', color='skyblue', figsize=(10, 6))
    ax.set_title('Phổ điểm môn ' + show_name)
    ax.set_xlabel('Khoảng điểm')
    ax.set_ylabel('Số lượng học sinh')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y')
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
        plot_score_scatter(df, img_dir, "scatter_math_english.png")
        plot_avg_english_by_hometown(df, img_dir, "english_by_hometown.png")
        plot_math_score_distribution(df,'math_score', 'Toán', img_dir, 'math_score_distribution.png')
        plot_math_score_distribution(df,'literature_score', 'Văn', img_dir, 'literature_score_distribution.png')
        plot_math_score_distribution(df,'english_score', 'Tiếng Anh', img_dir, 'english_score_distribution.png')

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    # It is recommended to run main.py
    # This is for running the script directly from the 'analysis' directory
    analysis_data("cleaned_student_data.csv")
