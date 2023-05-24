from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request) :
    return render(request, 'stay/index.html')


from django.shortcuts import render, redirect
from django.conf import settings
from google.cloud import storage
import pymysql

connection = pymysql.connect(
    host=settings.DB_HOST,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME
)


def upload_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        variable = request.POST.get('variable')

        if image_file:
            # 구글 클라우드 스토리지에 이미지 업로드
            client = storage.Client.from_service_account_json(settings.GS_SERVICE_ACCOUNT_KEY_FILE)
            bucket = client.bucket(settings.GS_BUCKET_NAME)
            blob = bucket.blob(image_file.name)
            blob.upload_from_file(image_file, content_type=image_file.content_type)

            # 이미지 URL 생성
            image_url = f'https://storage.googleapis.com/{settings.GS_BUCKET_NAME}/{blob.name}'

            # 이미지 URL을 MySQL 등에 저장하고 필요한 로직을 수행

            with connection.cursor() as cursor:
                sql = "INSERT INTO stay_talbe (adress, people_num1) VALUES (%s, %s)"
                try:
                    variable = int(variable)
                except (ValueError, TypeError):
                    variable = None
                cursor.execute(sql, (image_url, variable))
                connection.commit()
            connection.close()

    return render(request, 'stay/upload_image.html')





