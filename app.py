import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb+srv://root:r00tUser@mycluster0-bpxqv.mongodb.net/task_manager?retryWrites=true&w=majority')

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    _tasks = mongo.db.tasks.find()
    task_list = [task for task in _tasks]
    return render_template("tasks.html", tasks = task_list)

# ADD
@app.route('/add_task')
def add_task():
    _categories = mongo.db.categories.find()
    categories_list = [categorie for categorie in _categories]
    return render_template('addtask.html', categories = categories_list)

@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))
    
# EDIT 
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('edittask.html', task=the_task,
                           categories=all_categories)


@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'categorie_name':request.form.get('categorie_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))

# DELETE
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))

# DISPLAY CATEGORIES
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
categories=mongo.db.categories.find())

# Edit category
@app.route('/edit_categorie/<categorie_id>')
def edit_categorie(categorie_id):
    return render_template('editcategory.html', categorie=mongo.db.categories.find_one({'_id': ObjectId(categorie_id)}))


# Update Category
@app.route('/update_categorie/<categorie_id>', methods=['POST'])
def update_categorie(categorie_id):
    mongo.db.categories.update(
        {'_id': ObjectId(categorie_id)},
        {'categorie_name': request.form.get('categorie_name')})
    return redirect(url_for('get_categories'))

# Delete category
@app.route('/delete_categorie/<categorie_id>')
def delete_categorie(categorie_id):
    mongo.db.categories.remove({'_id': ObjectId(categorie_id)})
    return redirect(url_for('get_categories'))
    
# Add category function
@app.route('/insert_categorie', methods=['POST'])
def insert_categorie():
    category_doc = {'categorie_name': request.form.get('categorie_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))

@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
debug=True)
