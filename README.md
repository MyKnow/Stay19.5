# Project : Stay19.5


## 프로젝트 로고
<br>


<p align="center">
    <img src="https://i.ibb.co/TB3Skx0/Kakao-Talk-Photo-2023-06-07-13-52-46.png" alt="Kakao-Talk-Photo-2023-06-07-13-52-46" width="200px" height="200px">
</p>
<br>


## 프로젝트 정보
>   팀명 : Stay19.5
>   개발 기간 : 2023.03 ~ 2023.06
<br>


## 팀원 및 역할 소개 :wave:
* 서원형 (단국대학교 모바일시스템공학과) : 데이터베이스 관리
* 손보경 (단국대학교 모바일시스템공학과) : UI 디자인
* 박범순 (단국대학교 모바일시스템공학과) : 인공지능 모델 구성 및 활용 로직 구현
* 정민호 (단국대학교 모바일시스템공학과) : API를 활용한 로그인, MAP 검색 및 카메라 촬영 기능 구현
<br>


## 프로젝트 소개
### :star: 개발 취지
최근 몇년간 10~20대 사이에서 인생네컷, 포토이즘 등의 포토부스 촬영하는 것이 매우 활성화되었다. 관련 수요가 늘어나며 이러한 사진을 보관하기 위한 수단을 찾고자하는 움직임이 증가하고 있다. 이에 사람들의 요구를 충족할 수 있는 관련 종합 플랫폼 형태의 웹사이트를 제작하고자 하였다.
    
### :star: 제공 기능
#### :point_right: 포토부스 위치 제공 서비스
* **지도 API를 통한 이용자 현재 위치 기반 포토부스 위치 정보 제공**

   
#### :point_right: 사진 갤러리
* **QR코드를 통한 사진 업로드**
* **사용자별 갤러리 기능 제공**
* **특정 인물과의 사진만 볼 수 있는 AI 갤러리 모드**
<br>


## 사용자 이용 가이드 :green_book:
1. '**로그인하기**' 버튼을 누르고 카카오톡 계정으로 로그인을 한다.


[![image.png](https://i.postimg.cc/V67YkppH/image.png)](https://postimg.cc/HcyGSZpQ) [![image.png](https://i.postimg.cc/vmpxX13v/image.png)](https://postimg.cc/5HSt2tcH)


2. 사용 목적에 따라 화면 아래쪽에 있는 네비게이션바에서 기능을 이용한다.


[![image.png](https://i.postimg.cc/VkKj9Lx7/image.png)](https://postimg.cc/4Yh7sZNt)


3. '**지도**' 버튼을 통해 가까운 포토부스 위치를 확인할 수 있다.


[![image.png](https://i.postimg.cc/cHS4rfFP/image.png)](https://postimg.cc/t1BHcnQz)


4. '**업로드**' 버튼을 눌러 사진 속 QR코드로 사진 업로드를 시도한다.


[![image.png](https://i.postimg.cc/7PXYZG0Q/image.png)](https://postimg.cc/c6gNDJDQ) [![image.png](https://i.postimg.cc/rFPV5Bh1/image.png)](https://postimg.cc/2VnNDKNy)


>   * 밝기가 너무 밝으면 인식이 잘 안될 수 있습니다.
>   * QR코드는 대부분 **48시간**까지 유효하니 빠르게 업로드해주셔야합니다.


5. 업로드 완료 후, '**갤러리**' 버튼을 눌러 사진을 확인한다.


[![image.png](https://i.postimg.cc/9FrVXxWr/image.png)](https://postimg.cc/PPs02Qvj)


6. '**갤러리**' 속 '**AI 갤러리**' 버튼으로 AI 갤러리 모드를 사용할 수 있다.


[![AI.png](https://i.postimg.cc/FzYqvBjv/AI.png)](https://postimg.cc/D4K5d5jp)


7. '**MY**' 버튼으로 개인 프로필 확인과 로그아웃을 할 수 있다.


[![MY.png](https://i.postimg.cc/QdGPLSVL/MY.png)](https://postimg.cc/ppCkzfDk)
<br>
<br>

## Git Clone을 통한 웹사이트 접속 :open_file_folder:


### 웹사이트 접속 준비
>   macOS의 경우
>   python으로는 설치 진행이 안되므로, **python3**로 진행한다.


1. **python 설치**
* [Download Python](https://www.python.org/downloads/, "Python Download")
2. **pip 확인**
```
$ pip
$ python -m pip install --upgrade pip
```


혹은


```
$ pip3
$ python -m pip3 install --upgrade pip
```


### 설치
```
$ cd (directory path to clone our github repository)
$ git clone https://github.com/myknow/stay19.5
```


### 요구 프로그램들 설치
```
$ python -m pip install -r requirements.txt
```


### 웹사이트 접속하기 (Django 이용)
1. **clone한 디렉토리로 접근한다.**
```
$ cd stay19.5
```
2. **다음 명령어를 실행한다.**
```
$ python manage.py runserver
```
3. **웹브라우저에 접속하여 다음 주소를 입력한다.** https://127.0.0.1:8000/login/ 
4. **위에 제시된 사용자 가이드를 따라 웹사이트를 이용한다.**
5. **종료 시, 터미널에서 *ctrl-C*를 입력하여 사용을 종료한다.**
>   macOS의 경우, **cmd-C**를 입력한다.
<br>


## Stacks
#### Environment
<img src="https://img.shields.io/badge/pycharm-000000?style=for-the-badge&logo=pycharm&logoColor=white"> <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"> <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">

#### Development
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/jquery-0769AD?style=for-the-badge&logo=jquery&logoColor=white"> <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white">

#### Communication
<img src="https://img.shields.io/badge/notion-000000?style=for-the-badge&logo=notion&logoColor=white">
