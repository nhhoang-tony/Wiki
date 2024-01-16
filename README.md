# A wikipedia website where pages are contributed by users

## To run the wiki locally

1. Clone the repo `git clone https://github.com/nhhoang-tony/Wiki.git`

2. Ensure you have Python installed on your system

3. Run `pip install -r requirements.txt` to install the project dependencies.

4. Run `echo $TZ > /etc/timezone` and `ln -snf /usr/share/zoneinfo/$TZ /etc/localtime` to set up timezone

5. Run `python manage.py runserver` to start the wiki