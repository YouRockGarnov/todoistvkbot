from TodoistVK import app


@app.route('/todoist_check', methods=['GET'])
def check():
    return 'Это CHECK!!!'