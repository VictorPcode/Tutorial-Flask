from flask_bootstrap import Bootstrap5
from flask import Flask, jsonify, make_response, request, redirect, render_template

app= Flask(__name__,template_folder="template", static_folder="static")
bootstrap = Bootstrap5(app)

todos = ['Comprar cafe', 'Solicitud de compra ', 'Enviar video al productor']

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hola'))
    response.set_cookie('user_ip', user_ip)
    
    return response
    
@app.route('/hola')
def hola():
    user_ip= request.cookies.get('user_ip')
    context= {'user_ip': user_ip,
          'todos': todos,}
    return render_template('/hola.html', **context)

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