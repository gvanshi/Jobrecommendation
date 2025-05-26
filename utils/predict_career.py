import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
import re

def extract_numeric_year(year_str):
    try:
        if isinstance(year_str, (int, float)):
            return int(year_str)
        match = re.search(r'\d+', str(year_str))
        return int(match.group()) if match else -1
    except:
        return -1

def load_model_and_encoders():
    students_df = pd.read_csv("data/students_data.csv")
    students_df['Year of Study'] = students_df['Year of Study'].apply(extract_numeric_year)
    students_df = students_df[students_df['Year of Study'] != -1]
    students_df['Year of Study'] = students_df['Year of Study'].astype(float)

    label_encoders = {}
    for col in ['Level of Study', 'Field of Study']:
        le = LabelEncoder()
        students_df[col] = le.fit_transform(students_df[col])
        label_encoders[col] = le

    scaler = StandardScaler()
    students_df[['Year of Study']] = scaler.fit_transform(students_df[['Year of Study']])

    return students_df, label_encoders, scaler

def predict_career(education, field, year, experience):
    try:
        _, label_encoders, scaler = load_model_and_encoders()
        with open("models/career_model.pkl", "rb") as f:
            model = pickle.load(f)

        edu_encoded = label_encoders['Level of Study'].transform([education])[0]
        field_encoded = label_encoders['Field of Study'].transform([field])[0]
        year_scaled = scaler.transform([[year]])[0][0]

        X = pd.DataFrame([[edu_encoded, field_encoded, year_scaled, experience]],
                         columns=['Level of Study', 'Field of Study', 'Year of Study', 'Experience'])

        pred = model.predict(X)
        return str(pred[0])

    except Exception as e:
        return f"Error: {str(e)}"
