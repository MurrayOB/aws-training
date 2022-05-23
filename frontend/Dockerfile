FROM node:15.14-alpine

WORKDIR /app

EXPOSE 3000

COPY package.json package-lock.json ./

#silent doesnt show processes
RUN npm install --silent

#copies all remaining files
COPY . ./

CMD ["npm", "start"]