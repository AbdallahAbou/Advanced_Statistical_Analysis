import sys
import os
sys.path.insert(1, os.path.abspath('../configs'))
import config # type: ignore
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

    def visualize_data(self):
        """
        Visualize the data using various plots.
        """
        # Check for missing values
        print(self.df.isnull().sum())

        # Plotting histograms
        self.df.hist(figsize=(10, 10))
        plt.show()

        # Correlation matrix
        corr_matrix = self.df.corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        plt.show()

        # Scatter plot for two variables
        sns.scatterplot(x='Körpergröße, cm', y='Gewicht, Kg', data=self.df)
        plt.show()

        # Box plot for categorical variable vs. numerical variable
        sns.boxplot(x='Geschlecht', y='BMI', data=self.df)
        plt.show()

        # Pair plot for multiple variables
        sns.pairplot(self.df[['Körpergröße, cm', 'Gewicht, Kg', 'BMI', 'Ruhepuls']])
        plt.show()
        
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
        
        return subset_df