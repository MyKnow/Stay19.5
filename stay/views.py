from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import random
from django.shortcuts import render, redirect
from django.conf import settings
from google.cloud import storage
import pymysql
from .models import Stay_model

connection = pymysql.connect(
    host=settings.DB_HOST,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME
)

def index(request):
    return render(request, 'stay/index.html')

@csrf_exempt
def upload_image(request):
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
            id_token = 8103

            nickname = "원형" #카카오 아이디 토큰 넣을거임

            # 이미지 URL을 MySQL 등에 저장하고 필요한 로직을 수행
            people_values = [random.randint(1, 100) for _ in range(10)]

            # 커서 생성
            with connection.cursor() as cursor:
                # 데이터 삽입 SQL 문 실행
                sql = "INSERT INTO stay_table (id_token, address, "
                for i in range(1, len(people_values) + 1):
                    sql += f"people_num{i}, "
                sql += "name) VALUES (%s, %s, "
                for _ in range(len(people_values) + 1):
                    sql += "%s, "
                sql = sql[:-2] + ")"
                data = (id_token, image_url,) + tuple(people_values) + (nickname,)
                cursor.execute(sql, data)

                # 변경 사항 커밋
                connection.commit()

            # 연결 종료
            connection.close()

    image_addresses = get_image_addresses()  # 이미지 주소들을 가져옴
    return render(request, 'stay/upload_image.html', {'image_addresses': image_addresses})

def get_image_addresses():
    # name이 "원형"인 테이블들의 address 필드 값 가져오기
    table_data = Stay_model.objects.filter(people_num1=1).values_list('address', flat=True)
    image_addresses = list(table_data)  # 이미지 주소들을 리스트로 변환

    return image_addresses