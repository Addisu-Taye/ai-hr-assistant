import pandas as pd
from io import BytesIO
from django.conf import settings
import os

import pandas as pd
from io import BytesIO
from django.conf import settings
import os

def clean_hr_data(file):
    """
    Loads HR data from a file, performs basic cleaning, and returns a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    print("Initial DataFrame:")
    print(df)

    numeric_cols = ['Age', 'Salary', 'Tenure', 'Satisfaction', 'AbsentDays']
    for col in numeric_cols:
        print(f"\nAttempting to convert column: {col}")
        for index, value in df[col].items():
            try:
                pd.to_numeric(value, errors='raise') # 'raise' will throw an error if conversion fails
            except ValueError as e:
                print(f"Error converting '{value}' in row {index} of column '{col}': {e}")
                return None # Stop processing if we find a conversion error
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Handle missing values AFTER attempting numeric conversion
    for col in numeric_cols:
        df[col].fillna(df[col].mean(), inplace=True)

    categorical_cols = ['Gender', 'Education', 'Department', 'Promotion']
    for col in categorical_cols:
        df[col].fillna(df[col].mode()[0], inplace=True)

    df.drop_duplicates(inplace=True)

    print("\nCleaned DataFrame (before saving):")
    print(df.head()) # Print the first few rows of the cleaned DataFrame

    return df


def save_cleaned_data_to_model(df):
    """
    Saves the cleaned pandas DataFrame to your HRData model (or a new model).
    """
    from .models import ProcessedHRData  # Assuming you'll create this model

    for index, row in df.iterrows():
        try:
            ProcessedHRData.objects.create(
                employee_id=row['EmployeeID'],
                department=row['Department'],
                gender=row['Gender'],
                age=row['Age'],
                education=row['Education'],
                salary=row['Salary'],
                tenure=row['Tenure'],
                satisfaction=row['Satisfaction'],
                absent_days=row['AbsentDays'],
                promotion=row['Promotion'] == 'Yes' # Convert 'Yes/No' to boolean
                # Add other fields as necessary based on your ProcessedHRData model
            )
        except Exception as e:
            print(f"Error saving row {index}: {e}")

def handle_uploaded_file(file):
    """
    Handles the uploaded file, cleans the data, and saves it to the database.
    """
    df = clean_hr_data(file)
    if df is not None:
        save_cleaned_data_to_model(df)
        return True
    return False