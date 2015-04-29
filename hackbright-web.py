from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)

@app.route("/")
def home_page():
    """Home page displaying a list of all students and a list of all projects, consisting of links."""

    student_list = hackbright.list_all_students()
    project_list = hackbright.list_all_projects()
    return render_template("index.html", student_list=student_list, project_list=project_list)

@app.route("/student-search")
def get_student_form():
    """Display a search box."""

    return render_template('student-search.html')

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')
    if github:
        first, last, github = hackbright.get_student_by_github(github)
        project_list = hackbright.get_all_project_grades(github)
        return render_template("student-info.html", first=first, last=last, github=github, project_list=project_list)
    else:
        return redirect('/student-search')

@app.route("/student-add-form")
def student_add_form():
    """Display a form for adding a new student."""

    return render_template('student-add-form.html')

@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    github = request.form.get('github')

    if firstname and lastname and github:
        hackbright.make_new_student(firstname, lastname, github)
        first, last, github = hackbright.get_student_by_github(github)
        return render_template("student-info.html", first=first, last=last, github=github)
    else:
        return redirect('/student-add-form')

@app.route('/project')
def get_project_info():
    """List information about a project."""

    title = request.args.get('title')
    description, max_grade = hackbright.get_project_by_title(title)
    student_grades_list = hackbright.get_students_and_grades(title)
    return render_template('project-info.html', title=title, description=description, 
        max_grade=max_grade, student_grades_list=student_grades_list)

if __name__ == "__main__":
    app.run(debug=True)