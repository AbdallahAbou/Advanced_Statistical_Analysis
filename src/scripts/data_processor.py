
import os
from configs import config
import pandas as pd
from fuzzywuzzy import process
import logging



class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        logging.basicConfig(level=logging.INFO)
        self.df = None

    def load_data(self):
        """
        Loads data from an Excel file.
        """
        print(os.path.abspath(__file__))
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATA_FILE_PATH = os.path.join(BASE_DIR, self.file_path)
        logging.info("Loading data from Excel file.")
        self.df = pd.read_excel(DATA_FILE_PATH)
        return self.df

    def combine_columns(self, col1_index, col2_index):
        """
        Combines two columns by filling NaN values in the first column with values from the second column.
        Drops the second column after combining.
        """
        logging.info(f"Combining columns: {col1_index} and {col2_index}")
        self.df.iloc[:, col1_index] = self.df.iloc[:, col1_index].combine_first(self.df.iloc[:, col2_index])
        self.df.drop(columns=[self.df.columns[col2_index]], inplace=True)

    def drop_empty_columns(self):
        """
        Drops columns that are entirely empty.
        """
        logging.info("Dropping empty columns.")
        self.df.dropna(axis=1, how='all', inplace=True)

    def set_headers(self, headers):
        """
        Sets new headers for the DataFrame and drops the first row.
        """
        logging.info("Setting new headers.")
        self.df.columns = headers
        self.df.drop(index=0, inplace=True)

    def correct_typos(self, value, compare_with_values):
        """
        Corrects typos in a value by finding the best match from a list of valid values.
        """
        if pd.isna(value):
            return None
        best_match = process.extractOne(value, compare_with_values, score_cutoff=80)
        if best_match:
            return best_match[0]
        return None

    def apply_corrections(self, target_column, compare_with_values):
        """
        Applies typo corrections to a specified column in the DataFrame.
        """
        logging.info(f"Applying typo corrections to {target_column}.")
        self.df[target_column] = self.df[target_column].apply(lambda x: self.correct_typos(x, compare_with_values))

    def standardize_data(self, column, std_unit, rel_unit):
        """
        Standardize the data in the specified column to the given unit.
        
        Parameters:
        column (str): The name of the column to standardize.
        std_unit (float): The unit to standardize to (e.g., 60 for per minute).
        rel_unit (float): The relative unit for the data (e.g., duration of the video in seconds).
        """
        logging.info(f"Standardizing data in column {column} to per {std_unit} seconds, relative to {rel_unit} seconds.")
        
        try:
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
            self.df[column] = self.df[column].apply(lambda x: (x / rel_unit) * std_unit if pd.notnull(x) else x)
        except Exception as e:
            logging.error(f"Error standardizing data in column {column}: {e}")

    def is_invalid(self, value, expected_type):
        """
        Checks if a value is invalid based on its expected type.
        """
        if pd.isnull(value):
            #logging.debug(f"Invalid value (NaN): {value}")
            return True
        try:
            if expected_type == 'numeric':
                numeric_value = pd.to_numeric(value, errors='coerce')
                if pd.isnull(numeric_value):
                    logging.debug(f"Invalid numeric value: {value} (type: {type(value)})")
                    return True
            elif expected_type == 'date':
                pd.to_datetime(value, errors='raise')
            elif expected_type == 'category' and not isinstance(value, str):
                logging.debug(f"Invalid category value: {value} (type: {type(value)})")
                return True
        except (ValueError, TypeError) as e:
            logging.debug(f"Error converting value: {value} to type {expected_type}: {e}")
            return True
        return False

    def custom_validations(self, row):
        """
        Runs custom validations on a row.
        Returns a list of invalid cell columns if any cell in the row is invalid, otherwise returns an empty list.
        """
        invalid_cells = []
        try:
            rechts_hand = pd.to_numeric(row['Handlänge Rechts (cm)'], errors='coerce')
            links_hand = pd.to_numeric(row['Handlänge Links (cm)'], errors='coerce')
            rechts_fuss = pd.to_numeric(row['Fußlänge Rechts (cm)'], errors='coerce')
            links_fuss = pd.to_numeric(row['Fußlänge Links (cm)'], errors='coerce')
            ruhepuls = pd.to_numeric(row['Ruhepuls'], errors='coerce')
            
            if pd.isnull(rechts_hand):
                invalid_cells.append('Handlänge Rechts (cm)')
            if pd.isnull(links_hand):
                invalid_cells.append('Handlänge Links (cm)')
            if pd.isnull(rechts_fuss):
                invalid_cells.append('Fußlänge Rechts (cm)')
            if pd.isnull(links_fuss):
                invalid_cells.append('Fußlänge Links (cm)')
            
            if rechts_hand > links_hand * 1.2 or links_hand > rechts_hand * 1.2:
                invalid_cells.append('Handlänge Rechts (cm)')
                invalid_cells.append('Handlänge Links (cm)')
            
            if rechts_fuss > links_fuss * 1.2 or links_fuss > rechts_fuss * 1.2:
                invalid_cells.append('Fußlänge Rechts (cm)')
                invalid_cells.append('Fußlänge Links (cm)')
            
            if pd.isnull(ruhepuls):
                invalid_cells.append('Ruhepuls')
            
            if ruhepuls < 30 or ruhepuls > 120:
                invalid_cells.append('Ruhepuls')

        except (ValueError, TypeError, KeyError) as e:
            invalid_cells.extend(row.index)
        
        return invalid_cells
    
    def correct_column(self):
        self.df = self.df[self.df['Geschlecht'].isin(['männlich', 'weiblich'])].copy()


    def get_invalid_rows(self, expected_types):
        """
        Gets rows that are invalid based on expected types and custom validations.
        """
        logging.info("Getting invalid rows.")
        self.expected_types = expected_types
        
        # Check for invalid rows based on expected types
        invalid_rows_type = self.df.apply(lambda row: any(self.is_invalid(row[col], self.expected_types[col]) for col in self.df.columns), axis=1)
        logging.info(f"Type-based invalid rows: {invalid_rows_type.sum()}")
        
        # Check for invalid rows based on custom validations
        invalid_rows_custom = self.df.apply(lambda row: bool(self.custom_validations(row)), axis=1)
        logging.info(f"Custom invalid rows: {invalid_rows_custom.sum()}")
        
        # Combine both invalid row checks
        combined_invalid_rows = invalid_rows_type | invalid_rows_custom
        logging.info(f"Combined invalid rows: {combined_invalid_rows.sum()}")
        
        return self.df[combined_invalid_rows]

    def mark_invalid_data(self, expected_types, placeholder="-"):
        """
        Marks invalid data in the DataFrame with a placeholder.
        """
        logging.info("Marking invalid data.")
        
        # Mark cells based on expected types
        for column in self.df.columns:
            self.df[column] = self.df[column].apply(lambda x: placeholder if self.is_invalid(x, expected_types.get(column, 'category')) else x)
        
        # Apply custom validations and mark individual cells
        for index, row in self.df.iterrows():
            invalid_cells = self.custom_validations(row)
            for col in invalid_cells:
                self.df.at[index, col] = placeholder
        
        return self.df

    def calculate_and_update_bmi(self):
        """
        Calculates and updates BMI in the DataFrame where BMI is missing.
        """
        logging.info("Calculating and updating BMI.")
        
        def calculate_bmi(row):
            try:
                if pd.isnull(row['BMI']) and not pd.isnull(row['Gewicht, Kg']) and not pd.isnull(row['Körpergröße, cm']):
                    weight = row['Gewicht, Kg']
                    height_m = row['Körpergröße, cm'] / 100  # Convert height from cm to m
                    bmi = weight / (height_m ** 2)
                    return round(bmi, 1)  # Round to one decimal place
            except (ValueError, TypeError) as e:
                logging.error(f"Error calculating BMI for row {row.name}: {e}")
                return row['BMI']
            return row['BMI']
        
        # Apply the calculate_bmi function to each row
        self.df['BMI'] = self.df.apply(calculate_bmi, axis=1)
        return self.df

    def convert_columns_to_numeric(self, columns):
        """
        Convert specified columns to numeric values, coercing errors to NaN.
        """
        logging.info("Converting specified columns to numeric values.")
        for column in columns:
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
            # Debug statement to check if the conversion worked
            logging.debug(f"Converted {column} to numeric. Dtype: {self.df[column].dtype}")
    
    def calculate_or_correct_age(self):
        """
        Calculates or corrects the age for rows with missing or incorrect 'Alter, Jahre' using 'Geb.-Datum'.
        """
        def calculate_age(birth_date):
            today = pd.to_datetime("today")
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        self.df['Geb.-Datum'] = pd.to_datetime(self.df['Geb.-Datum'], errors='coerce')

        # Iterate over the DataFrame rows
        for index, row in self.df.iterrows():
            if pd.notna(row['Geb.-Datum']):
                correct_age = calculate_age(row['Geb.-Datum'])
                if pd.isna(row['Alter, Jahre']) or row['Alter, Jahre'] != correct_age:
                    #logging.info(f"Correcting age for row {index}. Old value: {row['Alter, Jahre']}, New value: {correct_age}")
                    self.df.loc[index, 'Alter, Jahre'] = correct_age

        logging.info("Missing or incorrect ages calculated/corrected using 'Geb.-Datum'.")

    

    def save_to_excel(self, save_path=config.default_save_path, save_name=config.default_name):
        """
        Saves the DataFrame to an Excel file with the default name specified in config.py.
        Ensures that date columns are saved with the correct format.
        """

        if not save_name.endswith('.xlsx'):
            save_name += '.xlsx'
        
        # Define the full path to save the file in the specified directory
        save = os.path.join(save_path, save_name)

        logging.info(f"Saving DataFrame to {save}")

        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Use xlsxwriter for formatting
        xl_writer = pd.ExcelWriter(save, engine='xlsxwriter')
        self.df.to_excel(xl_writer, sheet_name='data', index=False)

        # Get the workbook and worksheet
        wb = xl_writer.book
        ws = xl_writer.sheets['data']

        # Define the date format and apply it to the 'Geb.-Datum' column
        date_style = wb.add_format({
            'num_format': 'mm/dd/yyyy',
            'font_name': 'Calibri',
            'font_size': 10})
        # Assuming 'Geb.-Datum' is the 5th column (E column)
        ws.set_column('E:E', None, date_style)
        
        # Save the file
        xl_writer.close()
        logging.info(f"DataFrame saved to {save}")




