# MY-API

How to use:

- Create .env file with this env variables
    ```sh
    SECRET_KEY=your_secret_key
    API_KEY=your_api_key
    ```
- run with docker
  ``` sh
  docker run -d --name container_name -p your_port:5000 --env-file=./.env krojas4/my-api:latest
  ```
- Run with docker-compose
- create a docker-compose.yml file
  ``` sh
  version: "3.3"
  services:
    api:
      image: my-api:latest
      ports:
        - 5000:5000
      env_file: 
        - ./.env
  ```
- run docker-compose
  ``` sh
  docker-compose up -d
  ```

