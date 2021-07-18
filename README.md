# Karma Shop

## Ecommerce WebSite

# How to run project locally ?

`Note: ` redis has to installed in machine. check this blog for install redis in ubuntu20.04 [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04)

1. [optional] make virtual enviornment
2. [optional] activate virtual enviornment
3. Download or clone this project
4. Go to project directory and run ` pip install -r requirments.txt`
5. start the celery worker using `celery -A ecomm worker -l INFO`
6. start django server `python manage.py runserver`
