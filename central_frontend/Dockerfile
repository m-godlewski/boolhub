# base image
FROM node:18-alpine

# copies required packages list
WORKDIR /app
COPY package.json .

# installs required node packages
RUN npm install
RUN npm i -g serve

# copies source code
COPY . .

# builds application
RUN npm run build

# exposes port
EXPOSE 3000

# runs server
CMD [ "serve", "-s", "dist" ]