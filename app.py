from flask import flash, jsonify, make_response, session, request, redirect, render_template, url_for
import unittest
from app import create_app
from app.forms import LoginForm

app= create_app()

todos = ['Comprar cafe', 'Solicitud de compra ', 'Enviar video al productor']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/inicio'))
    session['user_ip'] = user_ip
    
    return response

@app.route('/inicio', methods=['GET'])
def hola():
    user_ip= session.get('user_ip')
    username = session.get('username')
    context= {'user_ip': user_ip,
          'todos': todos,
          'username': username,
        }
    return render_template('hola.html', **context)

@app.errorhandler(404)
def error_notFound(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def error_server(error):
    return render_template('500.html', error=error)

@app.route('/show_me_error_500')
def response_500():
    return jsonify(result={"status": 500}), 500
    



if __name__ == '__main__':
    app.run(port= 3000, debug=True)