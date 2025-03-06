FROM python:3.11-buster


# 해당 디렉토리에 있는 모든 하위항목들을 현재 디렉토리로 복사 ,, 여기서 지정
COPY . .

# 환경변수
ARG STAGE
ENV STAGE=${STAGE}

# 필요한 패키지 및 의존성 파일 설치
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get clean && apt-get update

ENTRYPOINT []
CMD []
