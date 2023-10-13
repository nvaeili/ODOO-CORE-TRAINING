# Odoo Installation


## Requirements
 - Docker
     - [Ubuntu Linux](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
     - [Windows](https://docs.docker.com/docker-for-windows/install/)
 - Docker-compose
     - Linux: `sudo apt install docker-compose` 
     - Windows: already installed with Docker Desktop


## Getting Started
  
  ### Notes
  * Make sure you have sufficient free diskspace on your partition, recommendation around 2GB. Running docker-compose will eventually download 1.2GB at the minimum.

  * Make sure you have installed `docker` and `docker-compose` in your system

  ### Steps
  1. Clone / Download this repository `git clone {repo_url} odoo15`
  2. Open up terminal on the working directory `cd odoo15`
  3. Checkout odoo15 branch `git checkout odoo15`
  3. execute `docker-compose up -d`
  4. Open your browser


## Restoring Databases via command line
  1. `docker exec -i odoo15_db_1 createdb <DB_NAME> -O odoo -U odoo`
  2. `cat <BACKUP_FILE> | docker exec -i odoo15_db_1 psql -U odoo -d <DB_NAME>`


## Running SQL Commands to docker
  1. Connect to the SQL `docker exec -i odoo15_db_1 psql -U odoo -d <DB_NAME> `
  2. Execute commands i.e.
  `update res_users set password = 1 where id = 1;` 
  3. `\q` to quit

## Adding Modules
  1. Place the modules on the addons directory
  2. Then execute the update module commands

## Updating Modules
  1. modify `docker-compose.yml` file
  2. Add the command line following line
  ```yml
  services:
  web:
    image: odoo:15.0
    depends_on:
      - db
    command: odoo -d <DB_NAME> -u <MODULE_NAME>
    ports:
      - "8069:8069"
  ``` 

## Docker Commands

  1. If Dockerfile has changed, need to rebuild the docker container:
     `docker-compose up --build`

  2. If docker-compose.yml file has changed, need to exec:
     `docker-compose up`
     Optional parameter is -d for detach if you don't want to see the logs: `docker-compose up -d`

  3. If only Odoo/UHH Modules or code has changed, just pull latest source code and restart the Odoo docker container. No need to exec docker-compose up.
     Here's the command: `docker-compose restart web`

