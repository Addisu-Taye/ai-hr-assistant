# AI HR Assistant Project

This project is an AI-powered HR assistant built using Django and Python. It aims to streamline various HR tasks, starting with data management, analytics, and predictive modeling for employee turnover.

## Features

* **HR Data Upload and Cleaning:** Allows users to upload HR data from CSV or Excel files. The system performs basic data cleaning steps to ensure data quality.
* **Data Storage:** Cleaned HR data is stored in a PostgreSQL database using Django's ORM.
* **HR Analytics:** Provides basic HR metrics such as:
    * Average Salary
    * Employee Turnover Rate (currently a simplified example)
    * Average Salary by Department (visualized as a bar chart)
* **Employee Turnover Prediction (Proxy):** Implements a simple Logistic Regression model (using scikit-learn) to predict the likelihood of "promotion" as a proxy for employee retention.
* **User-Friendly Dashboard:** Presents key HR metrics and visualizations in an organized and easy-to-understand dashboard interface built with Bootstrap.

## Technologies Used

* **Python:** The primary programming language.
* **Django:** A high-level Python web framework.
* **Pandas:** A powerful data analysis and manipulation library.
* **scikit-learn:** A machine learning library for Python.
* **Matplotlib and Seaborn:** Libraries for data visualization.
* **PostgreSQL:** The relational database used for storing HR data.
* **Bootstrap:** A CSS framework for creating a responsive and stylish user interface.
* **Git:** Version control system.
* **GitHub:** Platform for hosting the Git repository.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Addisu-Taye/ai-hr-assistant.git
    cd ai-hr-assistant
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    source env/bin/activate  # On macOS/Linux
    env\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *(Note: You might need to generate a `requirements.txt` file if you haven't already. You can do this after installing the necessary libraries with `pip freeze > requirements.txt`)*

4.  **Set up PostgreSQL:**
    * Ensure you have PostgreSQL installed and running.
    * Create a database for this project (e.g., `ai_hr_db`).
    * Update the database settings in `ai_hr_assistant_project/settings.py` with your PostgreSQL connection details:

        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'ai_hr_db',
                'USER': '<your_db_user>',
                'PASSWORD': '<your_db_password>',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
        ```

5.  **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser (for Django admin):**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    Open your browser and navigate to `http://127.0.0.1:8000/` to access the application.

## Usage

1.  **Access the admin interface:** Go to `http://127.0.0.1:8000/admin/` and log in with the superuser credentials you created. You can manage the `ProcessedHRData` here if needed.
2.  **Upload HR Data:** Navigate to the `/hr_data/upload/` URL to upload your HR data file (CSV or Excel).
3.  **View Analytics:** Access the analytics dashboard at `/analytics/dashboard/` to see key HR metrics and the average salary by department chart.
4.  **View Turnover Prediction:** Go to `/analytics/turnover_prediction/` to see the results of the simple employee turnover prediction model.

## Future Enhancements

* Implement a more accurate employee turnover rate calculation using historical data.
* Develop more sophisticated machine learning models for turnover prediction with feature engineering and hyperparameter tuning.
* Add more HR analytics and visualizations (e.g., time to hire, cost per hire, employee satisfaction analysis).
* Implement user authentication and authorization.
* Create more interactive dashboards using JavaScript charting libraries.
* Integrate with other HR systems or APIs.
* Add more data cleaning and validation options during the upload process.

## Contributing

Contributions to this project are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

MIT License

## Contact

Addisu Taye
addtaye@gmail.com