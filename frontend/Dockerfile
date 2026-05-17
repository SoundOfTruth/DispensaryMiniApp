FROM node:22

WORKDIR /app

COPY package*.json ./

RUN npm i

COPY . ./

ENV VITE_API_URL=/api/

RUN npm run build


CMD [ "cp", "-r", "dist", "result_build" ]