# RESTful-API-project

Этот репозиторий - мой тестовый проект. В данном приложении применён обширный стек технологий, использующийся на реальных проектах.


## Стек технологий которые были использованы
- **python:3+**
- **FASTapi**
- **PostgreSQL**
- **Redis**
- **Celery & Flower**
- **prometheus + grafana**
- **pytest**: Для тестирования

## Запуск приложения

В репозитории есть файл `test.sql`, все команды из файла можно внести в локальную БД, для последующего тестирования эндпоинтов.

Для запуска FastAPI используется веб-сервер uvicorn. Команда для запуска выглядит так:  
```
uvicorn app.app_main.main:app --reload
```  
Ее необходимо запускать в командной строке, обязательно находясь в корневой директории проекта.

### Celery & Flower
Для запуска Celery используется команда  
```
celery --app=app.tasks.celery:celery worker -l INFO -P solo
```
Обратите внимание, что `-P solo` используется только на Windows, так как у Celery есть проблемы с работой на Windows.  
Для запуска Flower используется команда  
```
celery --app=app.tasks.celery:celery flower
```
### Dockerfile
Для запуска веб-сервера (FastAPI) внутри контейнера необходимо раскомментировать код внутри Dockerfile и иметь уже запущенный экземпляр PostgreSQL на компьютере.
Код для запуска Dockerfile:  
```
docker build .
```  
Команда также запускается из корневой директории, в которой лежит файл Dockerfile.

### Docker compose
Для запуска всех сервисов (БД, Redis, веб-сервер (FastAPI), Celery, Flower, Grafana, Prometheus) необходимо использовать файл docker-compose.yml и команды
```
docker compose build
docker compose up
```
Причем `build` команду нужно запускать, только если вы меняли что-то внутри Dockerfile, то есть меняли логику составления образа.

### Внимание!
Некоторые части системы могут не работать. Часть библиотек, которые были использованы в приложении, достаточно давно обновлялись. В связи с этим могут возникать те или иные ошибки.
