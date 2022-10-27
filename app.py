import unittest
from flask import jsonify,url_for, make_response,flash, session, request, redirect, render_template
from flask_login import login_required, current_user

from app import create_app
from app.forms import todoForm, DeleteTodoForm, UpdateTodoForm
from app.firesotre_service import get_todos,delete_todo, put_todo, get_users, update_todo

app= create_app()



@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)




@app.errorhandler(404)
def error_notFound(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def error_server(error):
    return render_template('500.html', error=error)

@app.route('/show_me_error_500') 
def response_500():
    return jsonify(result={"status": 500}), 500

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/inicio'))
    session['user_ip'] = user_ip
    
    return response

@app.route('/inicio', methods=['GET', 'POST'])
@login_required
def hola():
    user_ip= session.get('user_ip')
    username = current_user.id
    todo_form = todoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()
    
    context= {
            'user_ip': user_ip,
            'todos': get_todos(user_id=username),
            'username': username,
            'todo_form': todo_form,
            'delete_form': delete_form,
            'update_form': update_form
            
        }
    
    users = get_users()

    for user in users:
        print(user.id)
        print(user.to_dict()['password'])

    if todo_form.validate_on_submit():
        put_todo(username,todo_form.description.data)
        flash('Tu tarea se creo con éxito!')
        
        return redirect(url_for('hola'))
    
    return render_template('hola.html', **context)


@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)
    return redirect(url_for('hola'))


@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
     user_id = current_user.id
     update_todo(user_id=user_id, todo_id=todo_id, done=done)
     return redirect(url_for('hola'))
    
 
if __name__ == '__main__':
    app.run(port= 3000, debug=True)