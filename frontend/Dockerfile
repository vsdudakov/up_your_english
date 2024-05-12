# syntax=docker/dockerfile:1.2
FROM node:21-alpine as base

WORKDIR /frontend

COPY package.json package.json
COPY yarn.lock yarn.lock
RUN yarn install

COPY . .

ARG VITE_SERVER_DOMAIN
ENV VITE_SERVER_DOMAIN=${VITE_SERVER_DOMAIN}
ENV NODE_OPTIONS="--max-old-space-size=5120"

RUN yarn build

FROM nginx:stable-alpine3.17-slim as final

COPY --from=base /frontend/dist/ /var/www/html/
COPY --from=base /frontend/nginx.mime.types /etc/nginx/mime.types
COPY --from=base /frontend/nginx.conf /etc/nginx/nginx.conf
