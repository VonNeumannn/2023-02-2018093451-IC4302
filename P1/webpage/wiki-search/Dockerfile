# Establecer la imagen base
FROM node:20-alpine3.17 AS builder

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración de Node.js
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto de los archivos de la aplicación
COPY . .

# Construir la aplicación
RUN npm run build

# Establecer la imagen base para el servidor Nginx
FROM nginx:1.25.2-alpine

# Establecer el directorio de trabajo
WORKDIR /usr/share/nginx/html

# Eliminar archivos existentes
RUN rm -rf ./*

# Copiar los archivos de construcción desde la etapa del constructor
COPY --from=builder /app/build .

# Establecer el punto de entrada para Nginx
ENTRYPOINT [ "nginx","-g", "daemon off;" ]