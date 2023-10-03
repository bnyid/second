# 기존의 views.py 코드를 수정하여 상대 경로를 설정

from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.urls import reverse  # reverse 추가
import os
import PyPDF2

# 현재 views.py 파일의 위치를 기준으로 상대 경로 설정 (Views.py와 같은 폴더에서 Lesson_PDFs를 찾게됨)
current_dir = os.path.dirname(__file__)
pdf_dir = os.path.join(current_dir, "Lessonpdfs")

def index(request):
    pdf_files = get_pdf_list()
    return render(request, 'index.html', {'pdf_files': pdf_files})

def merge_pdf(request):
    if request.method == 'POST':
        selected_pdfs = request.POST.getlist('pdf_files')
        merger = PyPDF2.PdfMerger()

        for pdf in selected_pdfs:
            merger.append(os.path.join(pdf_dir, pdf))

        output_pdf_path = os.path.join(pdf_dir, 'merged.pdf')
        merger.write(output_pdf_path)
        merger.close()

        pdf_url = request.build_absolute_uri(reverse('serve_pdf'))  # serve_pdf가 뷰의 name이라고 가정
        return JsonResponse({'message': 'PDFs merged successfully', 'pdf_url': pdf_url})
    else:
        return JsonResponse({'message': 'Invalid request'})

def serve_pdf(request):
    pdf_path = os.path.join(pdf_dir, 'merged.pdf')
    
    f = open(pdf_path, 'rb')  # 파일을 열고 닫지 않습니다. FileResponse가 닫을 것입니다.
    return FileResponse(f, content_type='application/pdf')

def get_pdf_list():
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    return pdf_files

# 이렇게 수정하면, 'Lesson_PDFs' 폴더를 프로젝트의 views.py와 같은 위치에 두면 됩니다.
