FROM node:18.17.1-alpine

#현재 컨테이너 디렉토리 루트 경로명이 FE 이다.
WORKDIR /FE

# FE 전체 복사 -> FE 프로젝트 전체
COPY . ./

# 이건 docker-compose에서 포트 매핑 해줬으니까 안해도 됨
EXPOSE 9090

# 컨테이너 안에서 node_module 설치
RUN yarn install
RUN yarn build

# 컨테이너 내에서 서버 실행
CMD ["yarn", "preview"]