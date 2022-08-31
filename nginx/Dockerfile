FROM node:14 as build
WORKDIR /app

COPY ./client/app .
RUN yarn add node-gyp
RUN yarn install && yarn build




# Build step 2(Deploying build on NGINX)
FROM nginx:1.13
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
RUN rm -rf /usr/share/nginx/html/*
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf:ro
COPY --from=build /app/dist /usr/share/nginx/html