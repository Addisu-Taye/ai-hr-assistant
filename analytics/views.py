from django.shortcuts import render
from data_management.models import ProcessedHRData
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from django.shortcuts import render
from data_management.models import ProcessedHRData
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np
from django.db.models import Avg, Count


def employee_turnover_prediction(request):
    """Predicts the likelihood of 'promotion' (as a proxy for staying/leaving) using Logistic Regression."""
    queryset = ProcessedHRData.objects.all()
    df = pd.DataFrame.from_records(queryset.values())

    if df.empty:
        return render(request, 'analytics/turnover_prediction.html', {'error': 'No processed HR data available.'})

    features = ['department', 'gender', 'age', 'education', 'salary', 'tenure', 'satisfaction', 'absent_days']
    target = 'promotion'

    X = df[features]
    y = df[target].astype(int)

    categorical_features = ['department', 'gender', 'education']
    numerical_features = [col for col in features if col not in categorical_features]

    print("Categorical Features:", categorical_features)
    print("Numerical Features:", numerical_features)
    print("Columns in X (before preprocessing):", X.columns.tolist())

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('num', 'passthrough', numerical_features)  # Pass through numerical features
        ])

    X_processed = preprocessor.fit_transform(X)

    print("Feature names after fit_transform:", preprocessor.get_feature_names_out())

    processed_feature_names = preprocessor.get_feature_names_out()
    X_processed_df = pd.DataFrame(X_processed, columns=processed_feature_names)

    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

    model = LogisticRegression(solver='liblinear', random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    all_data_processed = preprocessor.transform(df[features])
    probabilities = model.predict_proba(all_data_processed)[:, 1]
    df['Probability_of_Staying'] = probabilities

    predictions_data = df[['employee_id', 'department', 'Probability_of_Staying']].to_dict('records')

    context = {
        'accuracy': f"{accuracy:.2f}",
        'predictions': predictions_data,
    }
    return render(request, 'analytics/turnover_prediction.html', context)

def average_salary(request):
    """Calculates the average salary of all employees."""
    average = ProcessedHRData.objects.aggregate(Avg('salary'))['salary__avg']
    context = {'average_salary': average if average is not None else 0}
    return render(request, 'analytics/average_salary.html', context)

def turnover_rate(request):
    """Calculates a basic turnover rate (example: number of separations / total employees).
    This is a simplified example and would need more sophisticated logic based on your data
    (e.g., tracking start and end dates).
    """
    total_employees = ProcessedHRData.objects.count()
    # For this example, let's assume 'Promotion' being False in the last period indicates a separation
    # This is a simplification and needs to be adjusted based on your actual data and how you track separations.
    separations = ProcessedHRData.objects.filter(promotion=False).count() # Example logic
    turnover = (separations / total_employees) * 100 if total_employees > 0 else 0
    context = {'turnover_rate': f"{turnover:.2f}%"}
    return render(request, 'analytics/turnover_rate.html', context)
def average_salary_by_department(request):
    """Calculates the average salary for each department and generates a bar chart."""
    # 1. Calculate average salary by department
    department_salaries = ProcessedHRData.objects.values('department').annotate(avg_salary=Avg('salary')).order_by('department')

    # 2. Prepare data for the plot
    departments = [item['department'] for item in department_salaries]
    salaries = [item['avg_salary'] for item in department_salaries]

    # 3. Create the bar chart using Seaborn and Matplotlib
    plt.figure(figsize=(10, 6))  # Adjust figure size as needed
    sns.barplot(x=departments, y=salaries, palette='viridis')
    plt.title('Average Salary by Department')
    plt.xlabel('Department')
    plt.ylabel('Average Salary')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
    plt.tight_layout()

    # 4. Save the plot to a BytesIO object (in memory)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # 5. Encode the image to base64 for embedding in the template
    graphic = base64.b64encode(image_png).decode('utf-8')

    context = {'chart_data': graphic}
    return render(request, 'analytics/average_salary_by_department.html', context)

def get_base64_chart(plt):
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graphic = base64.b64encode(image_png).decode('utf-8')
        return graphic

def average_salary_by_department_chart():
    department_salaries = ProcessedHRData.objects.values('department').annotate(avg_salary=Avg('salary')).order_by('department')
    departments = [item['department'] for item in department_salaries]
    salaries = [item['avg_salary'] for item in department_salaries]
    plt.figure(figsize=(10, 6))
    sns.barplot(x=departments, y=salaries, palette='viridis')
    plt.title('Average Salary by Department')
    plt.xlabel('Department')
    plt.ylabel('Average Salary')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return get_base64_chart(plt)

def employee_turnover_risk():
    queryset = ProcessedHRData.objects.all()
    df = pd.DataFrame.from_records(queryset.values())
    if df.empty:
        return []

    # (Your AI model logic here - for now, let's categorize based on 'Probability_of_Staying')
    # Assuming you have a 'Probability_of_Staying' column in your DataFrame
    risk_data = []
    for index, row in df.iterrows():
        probability = row.get('Probability_of_Staying', 0.5) # Default to medium risk
        risk_level = "High" if probability < 0.4 else "Medium" if probability < 0.7 else "Low"
        risk_data.append({
            'employee_id': row['employee_id'],
            'department': row['department'],
            'risk_level': risk_level
        })
    return risk_data

def dashboard(request):
    average_salary = ProcessedHRData.objects.aggregate(Avg('salary'))['salary__avg'] or 0
    employee_count = ProcessedHRData.objects.count()
    turnover_rate = "N/A (Implementation Needed)" # Replace with your actual calculation
    average_salary_chart = average_salary_by_department_chart()
    turnover_risk_data = employee_turnover_risk()

    context = {
        'average_salary': average_salary,
        'employee_count': employee_count,
        'turnover_rate': turnover_rate,
        'average_salary_by_department_chart': average_salary_chart,
        'turnover_risk': turnover_risk_data,
    }
    return render(request, 'analytics/dashboard.html', context)
   