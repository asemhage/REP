FROM node:20-alpine AS base

WORKDIR /app

COPY package.json package-lock.json* ./

# Install dependencies (ignoring lockfile to ensure all deps are installed)
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]

