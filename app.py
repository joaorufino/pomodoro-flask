
import re
from flask import Flask, render_template, url_for, redirect, request, flash
from redis import Redis
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a very secret string'

r = Redis(host="redis",port=6379)

@app.route('/')
@app.route('/ongoing')
def index():
    m = r.get("mode")
    m = int(m)
    if(m==1):
        t=1500
        tipo="work"
    else:
        t=480
        tipo="rest"
    n = r.get("time")
    n1 = int(time.time())
    n2 = t - (n1 - int(n))      
    return render_template('index.html', num=n2)

@app.route('/<int:num>s')
@app.route('/<int:num>')
def timer(num):
    return render_template('index.html', num=num)

@app.route('/custom', methods=['GET', 'POST'])
def custom():
    time = request.form.get('time', 180)
    # use re to validate input data
    m = re.match('\d+[smh]?$', time)
    if m is None:
        return redirect(url_for('index'))
    if time[-1] not in 'smh':
        return redirect(url_for('timer', num=int(time)))
    else:
        type = {'s': 'timer', 'm': 'minutes', 'h': 'hours'}
        return redirect(url_for(type[time[-1]], num=int(time[:-1])))


@app.route('/<int:num>m')
def minutes(num):
    return redirect(url_for('timer', num=num*60))


@app.route('/<int:num>h')
def hours(num):
    return redirect(url_for('timer', num=num*3600))

# todo pomodoro mode: loop a 25-5 minutes cycle
@app.route('/pomodoro')
def pomodoro():
    r.incr("pomodoro")
    n1=int(time.time())
    r.set("mode",1)
    r.set("time",n1)
    return redirect(url_for('timer', num=1500))

@app.route('/rest')
def rest():
    r.incr("rest")
    r.set("mode",0)
    n1=int(time.time())
    r.set("time", n1)
    return redirect(url_for('timer', num=480))

@app.errorhandler(404)
def page_not_fouond(e):
    return redirect(url_for('timer', num=404))
