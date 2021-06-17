import atexit
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from resources.gateway_check import Gateway

app = Flask(__name__)


def check_gateway_status():
    """ Function for updating weather on the app. """
    gateway = Gateway()
    gateway.check_gateway_status()
    print("Scheduler is alive!")

sched = BackgroundScheduler(daemon=True)
# These cron jobs handle gateway status check
sched.add_job(check_gateway_status,'interval',minutes=30)
sched.start()


# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: sched.shutdown(wait=False))

if __name__ == '__main__':
    # app.run(host='0.0.0.0',port=5000) # for local machine
    app.run(debug=True)
