# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG MODE=${MODE}
RUN if [ "$MODE" = "staging" ] ; then mv .env.staging .env.production ; fi
ARG APP_NAME=${APP_NAME}
RUN node update-manifest.js
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
RUN rm /etc/nginx/conf.d/default.conf
COPY production-nginx.conf /etc/nginx/conf.d/production.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
