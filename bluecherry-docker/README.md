# Bluecherry Docker

## Goal

The application is already ["dockerized"](https://github.com/bluecherrydvr/bluecherry-docker), but it make it user friendly the following needs to happen

- Seed the mysql database _once_ on a new install but never seed again after the initial seed (we must not seed again when running docker compose up). Currently several commands have to be run and docker have to be stopped. We need this to be a fluid 'docker compose up -d' that does all of the seeding and setup.

- Don't start the main image until a) the seed is complete and b) mysql is running

- Handle mysql updates between image releases (there may be small changes to the mysql table structure between releases...handle this nicely)....patches are usually stored like [this](https://github.com/bluecherrydvr/bluecherry-apps/blob/master/misc/sql/mysql-upgrade/3000010/increase_media_size_max.sh)

## Create and Upgrade DB

Creating and upgrading a database when using MySQL with Docker Compose involves several steps. 

When a MySQL container is started for the first time, a new database with the specified name will be created and initialized with the provided configuration variables. Furthermore, it will execute files with extensions .sh, .sql and .sql.gz that are found in /docker-entrypoint-initdb.d. Files will be executed in alphabetical order. You can easily populate your mysql services by mounting a SQL dump into that directory and provide custom images with contributed data. SQL files will be imported by default to the database specified by the MYSQL_DATABASE variable.

1. Create a Dockerfile for MySQL

You first need to create a Dockerfile for your MySQL database. This Dockerfile should be based on the official MySQL image from Docker Hub. You can then add any additional configuration or scripts that you need. Here's an example of what this might look like:

```
FROM mysql:8.0

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=yourpassword 
ENV MYSQL_DATABASE=yourdatabase
ENV MYSQL_USER=youruser
ENV MYSQL_PASSWORD=yourpassword

# Add a database population script
ADD ./sql-scripts/ /docker-entrypoint-initdb.d/
```

Here we're setting some environment variables to configure the MySQL server. The docker-entrypoint-initdb.d directory is a special directory in the MySQL Docker image. Any scripts in this directory will be automatically run the first time the container is started.

2. Create SQL scripts

In the above Dockerfile, we're adding SQL scripts from the sql-scripts directory on your host machine to the docker-entrypoint-initdb.d directory in the Docker image. You should create this directory and add your SQL scripts to it. For example, you might have a `init.sql` script to create your initial database structure and a `upgrade.sql` script to upgrade your database.

3. Create a Docker Compose file

Next, you need to create a Docker Compose file to define your services. Here's an example of what this might look like:

```
version: '3.8'

services:
  db:
    build: .
    volumes:
      - db_data:/var/lib/mysql
    restart: always

volumes:
  db_data: {}
```

Here we're defining a single service db that builds from the Dockerfile in the current directory. We're also defining a volume db_data that persists the data in the /var/lib/mysql directory.

4. Run Docker Compose

Once you have your Dockerfile and Docker Compose file set up, you can start your services with Docker Compose:

```
docker-compose up -d
```

This will start your services in detached mode. You can then interact with your MySQL database as needed.

5. Upgrading the Database

For upgrading the database, you could create a new Docker image with a script that performs the upgrade, and deploy this as a new service using Docker Compose. However, you should be careful with this approach, as it could result in data loss if not done correctly. It's recommended to backup your data before performing any database upgrades.

Alternatively, you could connect to the running MySQL container and perform the upgrade manually. This might be more appropriate if you need to perform complex migrations.

## Depend on

Docker Compose starts services in dependency order. In a distributed environment, however, a service being "up" doesn't necessarily mean it's ready to accept connections. To handle this, Docker Compose supports the depends_on option which can make sure one service starts before another.

For example, if you have a web application that depends on a MySQL database, you can define your Docker Compose file like this:

```
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: example
```

However, depends_on only waits for the container to start, not for the db to be ready to accept connections. The better way is to make your application resilient to these types of failures.

For example, you can set your application to wait for the database to become available before it starts. One common approach is to use a script as the entrypoint for your application that waits for the database to start before starting your application.

Here's an example of such a script:

```
#!/bin/bash
set -e

until mysqladmin ping -h"db" --silent; do
    sleep 1
done

exec "$@"
```

This script will use the mysqladmin ping command to check if the MySQL server is running. If it's not, it will sleep for 1 second and then try again. Once the MySQL server is running, it will start the application.

You can use this script as the entrypoint for your application in your Dockerfile:

```
FROM node:14
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
RUN chmod +x ./wait-for-db.sh
CMD [ "./wait-for-db.sh", "npm", "start" ]
```

In this Dockerfile, we're copying the wait-for-db.sh script into the Docker image and then using it as the entrypoint for the application. The npm start command (or whatever command starts your application) is passed as arguments to the wait-for-db.sh script and gets executed once the database server is up and running.

Remember to replace placeholders and commands with the ones that are relevant to your application and environment.

Keep in mind that this is a simple example and there are many other factors to consider when creating resilient applications, such as handling network failures and database downtime.

## Handle MySQL patching

Automatically patching a MySQL instance with an application image is a bad idea. Instead, you would typically apply database patches or upgrades manually or using a controlled process, to avoid potential issues or data loss.

I can also provide custom scripts to automatically patch a MySQL instance before running the application if needed.

## The Key

I think containerization technology is a good choice. Docker containers can run on any system that has Docker installed. This means you can run your applications on any machine, cloud service, or operating system that supports Docker.

The key to this task is how to initialize and upgrade the database and coordinate with the application in docker compose environment.
I suggest that all of the database, the data of application, the scripts of the data integrate with MySQL image. It's better to introduce database version control. The application not only needs to retry the database connection, but also needs to verify the version of the database. This will greatly improve application and database coordination.

In addition the script install.sh will setup docker compose configrature  including .env, and also setup email notification. And it will also check if docker is installed and check if email send successfully. But it doesn't provide the capablities to install docker and setup Mail Transfer Agent(MTA) becasue the process can vary between different systems and distributions.
