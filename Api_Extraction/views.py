from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from Api_Extraction.extraction import Extraction
import os
from  Api_Extraction.extraction_ai import extraction as ai
from recruitment_recommender_system.settings import BASE_DIR
import json
from .extraction import utils_nlp
dir_path = os.path.join(BASE_DIR,'Api_Extraction/cv')

extraction = Extraction(BASE_DIR)
@api_view(['GET'])
def extract_cv(request,pathfile):

    return Response(extraction.parse_cv(os.path.join(dir_path,pathfile)))


json_cv = {}
@api_view(['GET','POST'])
def Upload_CV(request):
    if request.method == 'POST' and request.FILES.get('file'):
        myfile = request.FILES['file']

        fs = FileSystemStorage()

        filename = fs.save('cv/'+myfile.name, myfile)

        result_json = (extraction.parse_cv(fs.path(filename)))
        result_json = utils_nlp.format_show(result_json)
        if len(result_json['image'])>0:
            url_image = '/'.join(os.path.split(result_json['image'][0].replace('\\','/'))[-2:])
            url_image =url_image[1:]
            result_json['image'] =  url_image
        url = fs.url(filename)
        json_cv.update(result_json)
        return render(request, 'templates/index.html', context={'msg':json.dumps(result_json, ensure_ascii=False),'state':'Upload successfully!'})
        print(request.content_type)
    print(request.content_type)
    return render(request, 'templates/index.html', context={'msg':json.dumps({}),'state':''})

@api_view(['POST','GET'])
def get_json(request):
    if request.method=='POST':
        data = request.POST
        json_cv['language_cv'] = data['language_cv']
        json_cv['person_details']['name'] =data['name']
        json_cv['person_details']['birth_day'] = data['birth_day']
        json_cv['person_details']['sex'] = data['sex']
        json_cv['person_details']['mail'] = data['mail']
        json_cv['person_details']['address'] =data['address']
        json_cv['person_details']['number'] = data['number']

        json_cv['education']['cpa'] = data['cpa']
        json_cv['education']['university'] = data['university']
        json_cv['education']['awards'] = data['awards']
        json_cv['education']['language'] = data['language']
        json_cv['education']['major'] = data['major']

        json_cv['skills']['programing'] =data['programing']
        return Response(json_cv)
    if request.method =='GET':
        return Response(json_cv)
    return render(request, 'templates/index.html', context={'msg': json.dumps({}), 'state': ''})

@api_view(['GET','POST'])
def demo(request):
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']

        fs = FileSystemStorage()

        filename = fs.save('cv/'+myfile.name, myfile)

        result_json = ai.predict (fs.path(filename))
        # result_json = utils_nlp.format_show(result_json)
        if len(result_json['image'])>0:
            url_image = '/'.join(os.path.split(result_json['image'][0].replace('\\','/'))[-2:])
            url_image =url_image[1:]
            result_json['image'] =  url_image
        url = fs.url(filename)
        json_cv.update(result_json)
        return render(request, 'templates/Info.html', context={'msg':json.dumps(result_json, ensure_ascii=False),'state':'Upload successfully!'})
        print(request.content_type)
    print(request.content_type)
    return render(request, 'templates/upload.html', context={'msg':json.dumps({}),'state':''})
