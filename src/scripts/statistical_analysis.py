import sys
import os
from configs import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # type: ignore

class StatisticalAnalysis:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
    
    def load_clean_data(self):
        """
        Load the clean data from an Excel file
        """
        self.df = pd.read_excel(self.file_path)
        return self.df
    
    def summarize_data(self):
        """
        Display basic information and summary statistics.
        """
        print(self.df.info())
        print(self.df.describe())

    def generate_subset(self, columns):
        """
        Generate a subset of the DataFrame based on specified columns.
        """
        # Ensure all specified columns exist in the DataFrame
        if not all(col in self.df.columns for col in columns):
            missing_cols = [col for col in columns if col not in self.df.columns]
            raise ValueError(f"Columns not found in DataFrame: {missing_cols}")
        
        # Filter out rows where any of the specified columns contain NaN
        subset_df = self.df.dropna(subset=columns)
        
        # Filter out rows where any of the specified columns contain placeholders
        subset_df = subset_df[~subset_df[columns].isin(['-', np.nan]).any(axis=1)]
        
        # Return only the relevant columns
        columns.append('Gruppe')
        columns.append('Gesamtgruppe')
        return subset_df[columns]
    
    # Function to calculate descriptive statistics
    def descriptive_stats(self, sub_df, columns):
        stats = sub_df[columns].describe().transpose()
        rounded_stats = stats.round(2)
        return rounded_stats
    
    def save_as_latex(self, sub_df, save_path, file_name):
        """
        Save DataFrame as a LaTeX table content.
        """
        file_path = f"{save_path}/{file_name}.tex"
        with open(file_path, 'w') as f:
            for row in sub_df.itertuples():
                row_data = f"{row[0]} & " + ' & '.join(map(str, row[1:]))
                f.write(f"{row_data} \\\\\n")

    def create_histogram(self, data, column, group_name, save_path=None):
        plt.figure(figsize=(10, 6))
        plt.hist(data[column], bins=20, edgecolor='black', alpha=0.7)
        plt.title(f'Histogramm von {column} - {group_name}')
        plt.xlabel(column)
        plt.ylabel('Häufigkeit')
        plt.grid(True)
        
        if save_path:
            filename = f"{save_path}/histogram_{group_name}_{column}.png"
            plt.savefig(filename)
            return filename
        
        plt.show()
        return None