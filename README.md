# Scanvideo
======================

# 1. Scanvideo 관하여
Next릴에 성인광고를 검출하거나 검출한 파일을 삭제 또는 지정한 디렉토리로 옮겨주는 프로그램 입니다.

# 2. 테스트 환경
* Debian Linux
* Python 3.x (2.x 지원안함)

# 3. Third-party Library (2017-04-16 기준)
* moviePy 0.2.3.1
* Pillow 4.0.0
* pytesseract 0.1.6

# 4. 설정 방법
3번의 항목들이 이미 설치되어 있는 경우 이 단계는 생략 가능합니다.

## Python 설치
    sudo apt-get install python3

## Third-party library 설치
    pip3 intsall moviepy pillow pytesseract
    
# 5. 실행 방법
#* 기본 실행방법은 아래와 같습니다.
    python3 scanvideo.py <파일명>
#* 비디오 파일에서 1, 3, 5, 40초 영상을 검사합니다.
    python3 scanvideo.py --f 1,3,5,40 <파일명>
#* 테스트 모드로써 비디오 파일의 모든 구간을 검사합니다. 모든 구간을 검사하기 때문에 시간이 오래 걸립니다. 이 모드를 통해 몇 초에서 성인광고가 나타는지 확인 가능하며, 확인 후 --f 옵션을 사용하여 해당 구간을 검사할 수 있습니다.
    python3 scanvideo.py --t <파일명>
#* find 명령어와 파이프를 통해 해당 경로의 하위 모든 파일에 대해 검사 합니다.
    find <검색할 경로> -type f | sed 's/[^[[:alnum:]]/\\&/g' | xargs python3 ./scanvideo.py
#* find 명령어와 파이프를 통해 해당 경로의 하위 모든 파일에 대해 검사 후 검출된 파일은 삭제합니다. 파일은 삭제 후 복구가 불가능합니다.
    find <검색할 경로> -type f | sed 's/[^[[:alnum:]]/\\&/g' | xargs python3 ./scanvideo.py --r
#* find 명령어와 파이프를 통해 해당 경로의 하위 모든 파일에 대해 검사 후 검출된 파일은 설정한 경로로 이동합니다.
    find <검색할 경로> -type f | sed 's/[^[[:alnum:]]/\\&/g' | xargs python3 ./scanvideo.py --i ./infected/
#* find 명령어와 파이프를 통해 해당 경로의 생성일자가 1일 전인 모든 파일에 대해 검사 후 검출된 파일은 삭제합니다. 파일은 삭제 후 복구가 불가능합니다.
    find <검색할 경로> -mtime -1 -type f | sed 's/[^[[:alnum:]]/\\&/g' | xargs python3 ./scanvideo.py --r
#* find 명령어와 파이프를 통해 해당 경로의 생성일자가 1일 전인 모든 파일에 대해 검사 후 검출된 파일은 설정한 경로로 이동합니다.
    find <검색할 경로> -mtime -1 -type f | sed 's/[^[[:alnum:]]/\\&/g' | xargs python3 ./scanvideo.py --i /var/www/infected/

