# Dockerfile for frontend
# Use Node.js image for React app
FROM node:20

# Set working directory
WORKDIR /app

# Copy the entire React app source code
COPY ./frontend .

# Install dependencies
RUN npm install

# Build the React app
RUN npm run build

# Serve the app on port 3000
EXPOSE 3000
CMD ["npx", "serve", "-s", "build", "-l", "3000"]