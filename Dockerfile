# add node version 20 to the image; specifies the base image
FROM node:20

# Sets the working directory inside the container
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Install Python dependencies if a requirements.txt file exists
RUN python -m pip install -r requirements.txt

# Install the frontend dependencies
WORKDIR /app/frontend
RUN npm install

# Install concurrently package to manage frontend and backend processes together
RUN npm install -g concurrently

# environment variable, so that the port can be accessed during runtime
ENV PORT1=3000 PORT2=5000

# EXPOSE backend and frontend ports
EXPOSE 3000 5000

# start app
CMD ["npm", "start"]