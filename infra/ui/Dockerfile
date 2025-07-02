# Stage 1: Build the React application
FROM node:24.3.0 AS build

WORKDIR .

COPY ./ui/package.json ./ui/package-lock.json ./

RUN npm install

COPY ./ui .

RUN npm run build

# Stage 2: Serve the React application with Nginx
FROM nginx:alpine

# Copy build artifacts
COPY --from=build dist /usr/share/nginx/html

# Correct nginx.conf path within Docker context relative to infra/ui
COPY infra/ui/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 5000

CMD ["nginx", "-g", "daemon off;"]
