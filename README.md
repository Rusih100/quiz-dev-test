## Инструкция по запуску приложения
_В данной инструкции приводится пример запуска приложения через Docker_ 

### 1. Загрузка репозитория
Загрузите репозиторий и перейдите в него.
```shell
git clone https://github.com/Rusih100/quiz-dev-test.git
```
```shell
cd quiz-dev-test
```

### 2. Установка переменных окружения
Создайте файл ```.env``` и заполните его по примеру ```.example.env```.  
Ниже приведен пример ```.example.env```.
```.dotenv
# Postgres
DB_MODE=dev
DB_DATABASE_NAME=quiz
DB_DRIVER=asyncpg
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 3. Соберите проект 
Приведенная ниже команда Docker собирает проект.
```shell
docker-compose build
```

### 4. Запустите проект
Приведенная ниже команда Docker запускает проект.
```shell
docker-compose up 
```