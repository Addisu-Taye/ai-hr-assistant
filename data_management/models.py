from django.db import models

class HRData(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)
    data_file = models.FileField(upload_to='hr_data/')
    # You might add more fields here to describe the data file

    def __str__(self):
        return f"Data uploaded on {self.upload_date.strftime('%Y-%m-%d %H:%M')}"

class ProcessedHRData(models.Model):
    employee_id = models.IntegerField()
    department = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    age = models.FloatField()
    education = models.CharField(max_length=100)
    salary = models.FloatField()
    tenure = models.FloatField()
    satisfaction = models.FloatField()
    absent_days = models.FloatField()
    promotion = models.BooleanField()
    # Add other relevant fields here

    def __str__(self):
        return f"Processed Data for Employee ID: {self.employee_id}"