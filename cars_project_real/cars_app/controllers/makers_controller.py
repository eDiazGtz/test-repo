from cars_app import app
from flask import render_template, redirect, request
from cars_app.models.maker import Maker

@app.route('/makers')
def maker_dashboard():
    if not 'user_id' in session:
        return redirect ('/')
    makers = Maker.get_all()
    return render_template('makers_dash.html', makers=makers)

@app.route('/makers/new')
def maker_new():
    if not 'user_id' in session:
        return redirect ('/')
    return render_template('makers_new.html')

@app.route('/makers/create', methods = ['POST'])
def maker_create():
    if not 'user_id' in session:
        return redirect ('/')
    Maker.save(request.form)
    return redirect('/makers')



# Restful Routing ---- API 
# Point to one object



# Show form to EDIT one obj
# Handle query to update one obj

# Delete ONE object

# Show All that Obj
@app.route('/makers')
def makers_dash():
    pass

# Show form to make new obj
@app.route('/makers/new')
def makers_new():
    pass

# Handle query to make new obj
@app.route('/makers/create', methods = ['POST'])
def makers_create(): 
    data = {
        'name' : request.form['name']
    }
    maker_id = Maker.save(data)
    return redirect(f'/makers/{maker_id}')

# Show ONE of that obj 00 route parameters
@app.route('/makers/<int:maker_id>')
def makers_show(maker_id):
    data = {
        'id' : maker_id
    }
    maker = Maker.get_one(data)
    return render_template('show_maker.html', maker = maker)


@app.route('/makers/<int:maker_id>/edit')
def makers_edit(makers_id):
    pass

@app.route('/makers/<int:maker_id>/update', methods = ['POST'])
def makers_update(maker_id):
    data = {
        'id' : maker_id,
        'name' : request.form['name']
    }
    Maker.update(data)
    return redirect(f'/makers/{maker_id}')

@app.route('/makers/<int:maker_id>/delete')
def makers_delete(maker_id):
    data = {
        'id' : maker_id
    }
    Maker.delete(data)
    return redirect('/makers')