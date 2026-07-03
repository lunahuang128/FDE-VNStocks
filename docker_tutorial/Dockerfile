FROM node:26.4.0

COPY package.json /app/
COPY src /app/

WORKDIR /app

RUN npm install 

CMD ["node", "server.js"]