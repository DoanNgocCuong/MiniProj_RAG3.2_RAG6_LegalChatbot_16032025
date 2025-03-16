# Use Node.js as the base image
FROM node:18-alpine as build

# Install networking tools
RUN apk add --no-cache curl iputils wget

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all files
COPY . .

# Build the app
RUN npm run build

# Production stage
FROM nginx:alpine

# Install networking tools in production image
RUN apk add --no-cache curl iputils wget

# Copy built files from build stage to nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx config
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# Expose port 30001
EXPOSE 30001

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
