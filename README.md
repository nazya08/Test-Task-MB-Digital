# Test Assignment for MB Digital
## Installation and Usage with Docker

Here's how to get the project up and running using Docker and Docker Compose with Poetry.

### Setup

1. Clone this repository:

    ```bash
    git clone git@github.com:nazya08/vpn_service_SheepFish.git
    ```

2. Copy `.env` file and fill environment variables:

    ```bash
    cp .env.example .env
    ```

3. Build Docker images:

    ```bash
    docker compose build
    ```

4. Run Docker images:

    ```bash
    docker compose up
    ```

Your application should now be running at `http://localhost:8000`.


## Installation and Usage without Docker

Here's how to get the project up and running using Poetry locally.

### Setup

1. Clone this repository:

    ```bash
    git clone git@github.com:nazya08/vpn_service_SheepFish.git
    ```

2. Copy `.env` file and fill environment variables:

    ```bash
    cp .env.example .env
    ```
3. Verify the Poetry installation:

    ```bash
    poetry --version
   ```
4. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

5. Activate the virtual environment:

    ```bash
    poetry shell
    ```
   
6. Apply database migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
   
7. Run the application:

    ```bash
    python manage.py runserver
    ```
   
Your application should now be running at `http://localhost:8000`.


## Licence

MIT License

Created by Nazar Filoniuk, email: filoniuk.nazar.dev@gmail.com