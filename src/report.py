import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class Reporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def generate_csv(self, candidates):
        df = pd.DataFrame(candidates)
        # Sort by total score descending
        df = df.sort_values(by="score", ascending=False)
        output_path = os.path.join(self.output_dir, "ranking.csv")
        df.to_csv(output_path, index=False)
        print(f"Ranking report saved to {output_path}")
        return df

    def plot_scores(self, df):
        plt.figure(figsize=(10, 6))
        sns.barplot(x="score", y="filename", data=df, palette="viridis")
        plt.title("Candidate Ranking Scores")
        plt.xlabel("Total Score (%)")
        plt.ylabel("Candidate")
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, "ranking_plot.png")
        plt.savefig(output_path)
        print(f"Plot saved to {output_path}")
