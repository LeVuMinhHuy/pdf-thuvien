import os
from django.http import JsonResponse
from django.shortcuts import render
from .utils import process_pdf_file

def index(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        processed_file = process_pdf_file(uploaded_file)

        if processed_file:
            response_data = {
                'processed_file': processed_file  # Return the processed file path
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'File processing failed'}, status=400)

    return render(request, 'index.html')
