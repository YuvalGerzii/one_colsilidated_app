# Bond.AI API Server Dockerfile
FROM node:18-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code (excluding node_modules via .dockerignore)
COPY . .

# Remove any local node_modules that might have been copied and reinstall
RUN rm -rf node_modules && npm install

# Expose port
EXPOSE 3000

# Start the server with ts-node using require register
CMD ["node", "-r", "ts-node/register", "index.ts"]
