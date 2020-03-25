FROM node:10
WORKDIR /app
COPY package.json /app/testing
RUN npm install
COPY . /app/testing
CMD [ "node", "pup.js" ]
EXPOSE 3000