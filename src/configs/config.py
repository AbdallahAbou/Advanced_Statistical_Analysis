#config.py

new_headers = [
    'Gesamtgruppe', 'Type', 'Gruppe', 'Geschlecht', 'Geb.-Datum', 'Alter, Jahre', 
    'Körpergröße, cm', 'Gewicht, Kg', 'BMI', 'Ruhepuls', 
    'Fußlänge Rechts (cm)', 'Fußlänge Links (cm)', 
    'Handlänge Rechts (cm)', 'Handlänge Links (cm)', 
    'Priorisierte Hand', 'Wassermenge (ml/Tag)', 
    'Stamina Rechts (s)', 'Stamina Links (s)', 
    'Luftanhalten (s)', 'Häufigkeit Blinzeln (/min)'
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
    'Häufigkeit Blinzeln (/min)': 'numeric'
}

numeric_columns = ['Gesamtgruppe', 'Gruppe', 'Alter, Jahre', 'Körpergröße, cm', 'Gewicht, Kg', 'BMI', 'Ruhepuls', 
                'Fußlänge Rechts (cm)', 'Fußlänge Links (cm)', 'Handlänge Rechts (cm)', 'Handlänge Links (cm)', 
                'Wassermenge (ml/Tag)', 'Stamina Rechts (s)', 'Stamina Links (s)', 'Luftanhalten (s)', 'Häufigkeit Blinzeln (/min)']

typos = ['männlich', 'weiblich', 'rechsthänder', 'linkshänder', 'beidhändig']


columns_q1 = ['BMI', 'Ruhepuls']
columns_q2 = ['Priorisierte Hand', 'Handlänge Rechts (cm)', 'Handlänge Links (cm)']
columns_q3 = ['Geschlecht', 'Wassermenge (ml/Tag)']
columns_q4 = ['Häufigkeit Blinzeln (/min)']
columns_q5 = ['Geschlecht', 'Häufigkeit Blinzeln (/min)']
columns_q6 = ['Körpergröße, cm', 'Luftanhalten (s)']
columns_q7 = ['Priorisierte Hand', 'Luftanhalten (s)']


file_path = '../data/raw/Urliste_Datenerhebung_WS23_24.xlsx'




default_name = 'cleaned_data.xlsx'
default_save_path = '../data/clean/'