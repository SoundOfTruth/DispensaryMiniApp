FROM node:22

ARG VITE_API_URL
ARG VITE_MEDIA_URL

WORKDIR /app

COPY package*.json ./

RUN npm i

COPY . ./

ENV VITE_API_URL=$VITE_API_URL
ENV VITE_MEDIA_URL=$VITE_MEDIA_URL

RUN npm run build

CMD [ "cp", "-r", "dist", "result_build" ]