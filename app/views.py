import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .utils import process_pdf_file

def index(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        processed_file_name, processed_file_content = process_pdf_file(uploaded_file)

        if processed_file_content:
            response = HttpResponse(processed_file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{processed_file_name}"'
            return response
        else:
            return JsonResponse({'error': 'File processing failed'}, status=400)

    return render(request, 'index.html')
