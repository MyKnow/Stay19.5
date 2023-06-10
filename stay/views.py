from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import random
from django.shortcuts import render, redirect
from django.conf import settings
from google.cloud import storage
import pymysql
from .models import Stay_model
import datetime
import sys
import os
import json
from .face_detection_and_recognition import *
from django.http import JsonResponse
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse


def main(request):
    id = request.session.get('id')
    nickname = request.session.get('nickname')
    thumbnail_image = request.session.get('image')

    return render(request, 'common/main.html', {'id': id, 'nickname': nickname, 'thumbnail_image': thumbnail_image})


def login(request):
    return render(request, 'common/login.html')


def info(request):
    # 세션에서 정보 가져오기
    id = request.session.get('id')
    nickname = request.session.get('nickname')
    thumbnail_image = request.session.get('image')

    return render(request, 'common/info.html', {'id': id, 'nickname': nickname, 'thumbnail_image': thumbnail_image})


def getcode(request):
    code = request.GET.get('code')
    # REST API를 이용해 토큰 발급 받아옴 (카카오에게)
    requests.post('https://kauth.kakao.com/oauth/token')
    data = {'grant_type': "authorization_code",
            'client_id': 'aa4f2cb7ffd0e8ced07032bfa9361f57',
            'redirect_uri': 'http://127.0.0.1:8000/oauth/redirect',
            'code': code}
    headers = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    res = requests.post('https://kauth.kakao.com/oauth/token', data=data, headers=headers)
    token_json = res.json()
    print(token_json)

    # REST API를 이용해 토큰으로 정보를 조회
    access_token = token_json['access_token']

    headers = {'Authorization': 'Bearer ' + access_token,
               'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    res = requests.get("https://kapi.kakao.com//v2/user/me", headers=headers)
    profile_json = res.json()

    id = profile_json['id']  # ID 뽑아내기
    nickname = profile_json['properties']['nickname']  # 닉네임 뽑아내기
    image = profile_json['properties']['profile_image']  # 이미지 뽑아내기
    print(id)
    print(nickname)
    print(image)

    request.session['id'] = id
    request.session['nickname'] = nickname
    request.session['image'] = image

    return redirect('main')

def gallery(request):
    return render(request, 'gallery/gallery.html')

def photo(request):
    return render(request, 'gallery/photo.html')

def map(request):
    return render(request, 'map/map.html')

connection = pymysql.connect(
    host=settings.DB_HOST,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME
)

detect_onnx_file = os.path.join(settings.STAY_APP_DIR, 'ai_model', 'face_detection_yunet_2022mar.onnx')
recognize_onnx_file = os.path.join(settings.STAY_APP_DIR, 'ai_model', 'face_recognition_sface_2021dec.onnx')

def index(request):
    return render(request, 'qr/index.html')

@csrf_exempt
def upload_image(request):
    sys.path.append('http://127.0.0.1:8000/')
    print(request)
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        print(image_file)
        if image_file:
            # 구글 클라우드 스토리지에 이미지 업로드
            client = storage.Client.from_service_account_json(settings.GS_SERVICE_ACCOUNT_KEY_FILE)
            bucket = client.bucket(settings.GS_BUCKET_NAME)
            blob = bucket.blob(image_file.name)
            blob.upload_from_file(image_file, content_type=image_file.content_type)

            # 이미지 URL 생성
            image_url = f'https://storage.googleapis.com/{settings.GS_BUCKET_NAME}/{blob.name}'
            id_token = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            people_values = [[0] * 15 for _ in range(6)]
            results = facial_recognition_model(image_url)

            for i, result in enumerate(results):
                if i < len(people_values):
                    result_list = result.tolist()  # float32 값을 float 리스트로 변환
                    people_values[i] = result_list
                else:
                    break
            print(people_values)

            # 이미지 URL을 MySQL 등에 저장하고 필요한 로직을 수행

            # 커서 생성

            with connection.cursor() as cursor:
                # 데이터 삽입 SQL 문 실행
                sql = "INSERT INTO real_final_stay2 (address, people_1, people_2, people_3, people_4, people_5, people_6) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data = (image_url, *[json.dumps(value) for value in people_values[:6]])
                cursor.execute(sql, data)
                #n 번째 adress 값 image_url, people_values[1]이 15개 배열
                # 변경 사항 커밋
                connection.commit()

            id_num = get_id_num(image_url)[0]
            print(id_num)
            print(image_url)

            # (DB에 새롭게 넣을) 업로드된 사진에 대한 Label과 얼굴 정보 쌍들에 대한 리스트
            new_labels = [-1 for _ in range(len(results))]
            '''
            for 문 : 모든 사진에 대해 현재 업로드된 사진과 비교
            for 문 결과
            : labels_and_faces = [[people_1_number, people_1_values], [people_2_number, people_2_values], ...]
            - for 문 종료 후, 새로운 반복문을 통해 people_number == -1 인 경우, 새로운 label값 (max_val) 부여 후 label += 1
            - 모든 얼굴 정보에 대한 label값 부여 완료 후, people_number, people_value 부여
            
            '''
            for i in range(41,id_num): # 41번째 테이블 부터 시작해서 그럼
                image_addresses = get_field_values(Stay_model, 'address', i)
                people_1_values = get_field_values(Stay_model, 'people_1', i)
                people_2_values = get_field_values(Stay_model, 'people_2', i)
                people_3_values = get_field_values(Stay_model, 'people_3', i)
                people_4_values = get_field_values(Stay_model, 'people_4', i)
                people_5_values = get_field_values(Stay_model, 'people_5', i)
                people_6_values = get_field_values(Stay_model, 'people_6', i)
                prople_1_number = get_field_values(Stay_model, 'people_1_val', i)
                prople_2_number = get_field_values(Stay_model, 'people_2_val', i)
                prople_3_number = get_field_values(Stay_model, 'people_3_val', i)
                prople_4_number = get_field_values(Stay_model, 'people_4_val', i)
                prople_5_number = get_field_values(Stay_model, 'people_5_val', i)
                prople_6_number = get_field_values(Stay_model, 'people_6_val', i)
                db_faces = [
                    people_1_values,
                    people_2_values,
                    people_3_values,
                    people_4_values,
                    people_5_values,
                    people_6_values
                ]
                db_labels = [
                    prople_1_number,
                    prople_2_number,
                    prople_3_number,
                    prople_4_number,
                    prople_5_number,
                    prople_6_number
                ]

                if image_addresses:
                    image_addresses = image_addresses[0]  # 대괄호 제거
                else :
                    image_addresses = image_url
                new_labels = compare_with_other_images(image_addresses, db_faces, db_labels, image_url, results, new_labels)
                # DB 속 이미지 한 장 비교 완료

            # 새로 부여된 label 리스트 길이를 6으로 맞추기 (0으로)
            if(len(new_labels) < 6):
                for i in range(6 - len(new_labels)):
                    new_labels.append(0)
            people_1_val_exists = bool(Stay_model.objects.filter(people_1_val__isnull=False))
            max_value = 0  # 변수 초기화
            if people_1_val_exists:
                max_value = get_max_value_across_fields(Stay_model)

            #레이블 넘겨주면 그걸 데이터베이스 안에다가 넣고 리스트 값이 -1이면 max value+1
            # 리스트 전부가져와서 현재 id의 val값에다가 값 넣고 -1일 경우 max_value+1해서 넣어주기
            with connection.cursor() as cursor:
                values_list = new_labels  # 예시로 주어진 값들
                updated_values = []
                for value in values_list:
                    if value == -1:
                        max_value += 1  # max_val 값 증가
                        updated_values.append(max_value)
                    else:
                        updated_values.append(value)

                sql = "UPDATE real_final_stay2 SET people_1_val = %s, people_2_val = %s, people_3_val = %s, people_4_val = %s, people_5_val = %s, people_6_val = %s WHERE id = %s"
                data = tuple(updated_values[:6]) + (id_num,)
                cursor.execute(sql, data)

                # 변경 사항 커밋
                connection.commit()
    connection.close()# 연결 종료

    #image_addresses = get_image_addresses()  # 이미지 주소들을 가져옴
    #return render(request, 'stay/upload_image.html', {'image_addresses': image_addresses})
    return render(request,'stay/upload_image.html')

def get_field_values(model_class, field_name, n):
    # 모델 클래스와 필드 이름, n 값을 입력받아 해당 필드의 모든 값을 가져오기
    field_data = model_class.objects.filter(id=n).exclude(**{f"{field_name}__isnull": True}).values_list(field_name, flat=True)
    field_values = list(field_data)  # 필드 값들을 리스트로 변환

    return field_values

def get_id_num(image_url):
    # address가 "image_url"인 테이블들의 id 필드 값 가져오기, 즉 현재 id값 받아오기
    table_data = Stay_model.objects.filter(address=image_url).values_list('id', flat=True)
    id_num = list(table_data)  # 이미지 주소들을 리스트로 변환

    return id_num

from django.shortcuts import render
from .models import Stay_model

def show_images_by_val(request):
    # 숫자별 이미지 URL을 저장할 딕셔너리 생성
    image_urls_by_val = {}

    # 모든 필드 값에 대해 people_value의 최대값 조사
    for field_name in ['people_1_val', 'people_2_val', 'people_3_val', 'people_4_val', 'people_5_val', 'people_6_val']:
        field_values = get_field_values(Stay_model, field_name)
        max_val = max(max_val, max(field_values))

    # 1부터 max_val까지의 값에 대해 이미지 URL 저장
    for val in range(1, max_val + 1):
        image_urls = []
        for field_number in range(1, 7):
            field_name = f'people_{field_number}_val'
            records = Stay_model.objects.filter(**{field_name: val, 'image_url__isnull': False})
            image_urls += [record.image_url for record in records]

        image_urls_by_val[val] = image_urls

    return render(request, 'upload_image.html', {'image_urls_by_val': image_urls_by_val, 'max_val': max_val, 'val': request.GET.get('val', 1)})

def get_max_value_across_fields(model):
    """
    주어진 모델과 필드 이름들에 해당하는 필드 값들 중 최대값을 반환하는 함수
    """
    field_names = ['people_1_val', 'people_2_val', 'people_3_val', 'people_4_val', 'people_5_val', 'people_6_val']
    max_val = 0
    for field_name in field_names:
        field_values = model.objects.values_list(field_name, flat=True)
        field_values = [int(value) for value in field_values if str(value).isdigit()]  # 문자열을 정수로 변환하여 필드 값들을 가져옴
        max_val = max(max_val, max(field_values, default=0))
    return max_val

def get_image_urls(request):
    # 데이터베이스에서 이미지 URL 조회
    image_urls = Stay_model.objects.values_list('address', flat=True)

    # 이미지 URL을 리스트로 변환하여 JSON 응답으로 반환
    return JsonResponse(list(image_urls), safe=False)

def ai_gallery(request):
    stays = Stay_model.objects.all()
    addresses = []  # 주소 리스트 초기화
    k_list = []
    for stay in stays:
        address_row = []  # 주소 행 초기화
        k = 1
        while k <= get_max_value_across_fields(Stay_model):  # 1부터 10까지 반복
            found = False  # 해당하는 값이 있는지 여부 확인을 위한 변수
            for i in range(1, 7):  # 1부터 6까지 반복
                field_name = f"people_{i}_val"
                face_list = f"people_{i}"
                face_value = getattr(stay,face_list)
                if hasattr(stay, field_name):  # 필드가 존재하는지 확인
                    value = getattr(stay, field_name)
                    if int(value) == k and int(value) not in k_list:  # k 값과 일치하는 경우
                        address_row.append(stay.address)
                        k_list.append(k)
                        print(face_value)
                        # k = 1 일경우 value 1,  리스트 값= f"people_i"
                        crop_img_and_save(k, stay.address, face_value)
                        found = True  # 해당하는 값이 있음을 표시
                        break
            k += 1
        for address in address_row:
            addresses.append(address)
    context = {
        'addresses': addresses,
    }
    return render(request, 'gallery/ai_gallery.html', context)


def image_detail(request, image_id):
    image_id = int(image_id)  # image_id를 정수로 변환

    stays = Stay_model.objects.all()
    urls = []

    for stay in stays:
        for i in range(1, 7):
            field_name = f"people_{i}_val"
            if hasattr(stay, field_name):
                value = getattr(stay, field_name)
                if int(value) == int(image_id):
                    urls.append((stay.address, image_id))
                    break
    context = {
        'urls': urls,
    }

    return render(request, 'gallery/photo.html', context)
