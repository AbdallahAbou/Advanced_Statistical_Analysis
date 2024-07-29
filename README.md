# Advanced Statistics Analysis

The main goals of this project are to clean, analyze, and visualize data to answer various statistical questions.

## Project Structure:

```
.
├── data
│   ├── clean
│   │   └── cleaned_data.xlsx
│   └── raw
│       └── Urliste_Datenerhebung_WS23_24.xlsx
├── notebooks
│   ├── data_cleaning_notebook.ipynb
│   └── statistical_study_notebook.ipynb
├── src
│   ├── configs
│   │   ├── __init__.py
│   │   └── config.py
│   ├── scripts
│   │   ├── __init__.py
│   │   ├── data_processor.py
│   │   └── statistical_analysis.py
│   ├── __init__.py
│   └── data_cleaning.py
├── .gitignore
├── README.md
└── requirements.txt

```

## Setup:

1\. Clone the repository:

```bash
git clone https://github.com/AbdallahAbou/Advanced_Statistics_Analysis.git
```

2\. Navigate to the project directory:

```bash
cd Advanced_Statistics_Analysis
```

3\. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage:

- Data Processing and Cleaning:

 Run data_cleaning.ipynb to clean and preprocess the data, a new Excel file should be created in ./data/clean/.

```bash
jupyter notebook notebooks/data_cleaning.ipynb 
```

- Analysis and Visualization:

 Use the Jupyter notebook statistical_study.ipynb for data analysis and visualization.

```bash
jupyter notebook notebooks/statistical_study.ipynb
```

## Contributing:

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License:
    
This project is licensed under the MIT License - see the LICENSE file for details.
