from .import bp as social 
from flask import render_template, request
from flask_login import login_required, current_user

@social.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    if request.method =='POST': 
        return "'A' for effort"
    return render_template('index.html.j2')

