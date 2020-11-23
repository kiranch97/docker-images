# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG APP_NAME=${APP_NAME}
ENV VUE_APP_API_HTTP_URL=$API_HTTP
ENV VUE_APP_API_WS_URL=$API_WS
RUN node update-manifest.js
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
RUN rm /etc/nginx/conf.d/default.conf
COPY production-nginx.conf /etc/nginx/conf.d/production.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
