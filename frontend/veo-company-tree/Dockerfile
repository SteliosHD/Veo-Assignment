# ==== CONFIGURE =====
# Use a Node 18 base image

FROM node:18-alpine 

# setup environment variable
ENV DockerHOME=/home/app/veo_frontend

# set work directory
RUN mkdir -p $DockerHOME

# Set the working directory to /veo_app inside the container
WORKDIR $DockerHOME

# Copy app files
COPY . $DockerHOME

# ==== BUILD =====
# Install dependencies (npm ci makes sure the exact versions in the lockfile gets installed)
RUN npm ci 

# ==== RUN =======
ENV DEBUG false
# Expose the port on which the app will be running (3005 is  our default port)
EXPOSE 3005
# Start the app
CMD npm run start
