from django.shortcuts import render, redirect
from .forms import UploadDataForm
from django.contrib import messages
from .utils import handle_uploaded_file

def upload_data(request):
    if request.method == 'POST':
        form = UploadDataForm(request.POST, request.FILES)
        if form.is_valid():
            hr_data_instance = form.save() # Save the uploaded file instance
            if handle_uploaded_file(hr_data_instance.data_file):
                messages.success(request, 'Data uploaded and processed successfully!')
                return redirect('upload_data')
            else:
                messages.error(request, 'Error processing the uploaded data.')
        else:
            messages.error(request, 'There was an error in your upload.')
    else:
        form = UploadDataForm()
    return render(request, 'data_management/upload_data.html', {'form': form})