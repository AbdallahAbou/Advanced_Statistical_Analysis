from scripts.data_processor import DataProcessor
import configs.config as config
import pandas as pd
import numpy as np
from IPython.display import display


def main():

    processor = DataProcessor(config.file_path)
    df = processor.load_data()

    processor.combine_columns(17, 18)
    processor.drop_empty_columns()
    processor.set_headers(config.new_headers)
    processor.apply_corrections('Geschlecht', config.typos)
    processor.apply_corrections('Priorisierte Hand', config.typos)

    processor.df.loc[:75, 'Type'] = 'Studierende'
    processor.df.loc[76:, 'Type'] = 'simulierte Daten'
    processor.df.loc[:75, 'Gruppe'] = 1
    

    processor.calculate_and_update_bmi()
    processor.calculate_or_correct_age()
    processor.correct_column()
    processor.convert_columns_to_numeric(config.numeric_columns)
    processor.standardize_data('Häufigkeit Blinzeln (/min)', std_unit=60, rel_unit=116)



    df_invalid = processor.get_invalid_rows(config.expected_types)

    processor.mark_invalid_data(config.expected_types, placeholder=np.nan)


    # Save the DataFrame
    processor.save_to_excel()

    pd.set_option('display.max_rows', None)  
    pd.set_option('display.max_columns', None)  
    pd.set_option('display.width', None)  
    pd.set_option('display.max_colwidth', None)
    #display(processor.df)


if __name__ == "__main__":
    main()
