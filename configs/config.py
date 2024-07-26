#config.py

new_headers = [
    'Gesamtgruppe', 'Type', 'Gruppe', 'Geschlecht', 'Geb.-Datum', 'Alter, Jahre', 
    'Körpergröße, cm', 'Gewicht, Kg', 'BMI', 'Ruhepuls', 
    'Fußlänge Rechts (cm)', 'Fußlänge Links (cm)', 
    'Handlänge Rechts (cm)', 'Handlänge Links (cm)', 
    'Priorisierte Hand', 'Wassermenge (ml/Tag)', 
    'Stamina Rechts (s)', 'Stamina Links (s)', 
    'Luftanhalten (s)', 'Häufigkeit Blinken'
]

expected_types = {
    'Gesamtgruppe': 'numeric',
    'Type': 'category',
    'Gruppe': 'numeric',
    'Geschlecht': 'category',
    'Geb.-Datum': 'date',
    'Alter, Jahre': 'numeric',
    'Körpergröße, cm': 'numeric',
    'Gewicht, Kg': 'numeric',
    'BMI': 'numeric',
    'Ruhepuls': 'numeric',
    'Fußlänge Rechts (cm)': 'numeric',
    'Fußlänge Links (cm)': 'numeric',
    'Handlänge Rechts (cm)': 'numeric',
    'Handlänge Links (cm)': 'numeric',
    'Priorisierte Hand': 'category',
    'Wassermenge (ml/Tag)': 'numeric',
    'Stamina Rechts (s)': 'numeric',
    'Stamina Links (s)': 'numeric',
    'Luftanhalten (s)': 'numeric',
    'Häufigkeit Blinken': 'numeric'
}

numeric_columns = ['Gesamtgruppe', 'Gruppe', 'Alter, Jahre', 'Körpergröße, cm', 'Gewicht, Kg', 'BMI', 'Ruhepuls', 
                'Fußlänge Rechts (cm)', 'Fußlänge Links (cm)', 'Handlänge Rechts (cm)', 'Handlänge Links (cm)', 
                'Wassermenge (ml/Tag)', 'Stamina Rechts (s)', 'Stamina Links (s)', 'Luftanhalten (s)', 'Häufigkeit Blinken']

typos = ['männlich', 'weiblich', 'rechsthänder', 'linkshänder', 'beidhändig']


file_path = '../data/raw/Urliste_Datenerhebung_WS23_24.xlsx'


default_name = 'cleaned_data.xlsx'
save_path = '../data/clean/'