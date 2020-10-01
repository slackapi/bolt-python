```
pip install -r requirements.txt
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***

python manage.py migrate
python manage.py runserver 0.0.0.0:3000
```