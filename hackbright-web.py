from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)



@app.route("/")
def show_homepage():
    """Lists students and projects"""

    student_list = hackbright.display_students()
    project_list = hackbright.display_projects()

    return render_template("homepage.html", student_list=student_list, 
                                            project_list=project_list)

@app.route("/student-search")
def get_student_form():
    return render_template("student_search.html")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    projects = hackbright.get_grades_by_github(github)
    html = render_template("student_info.html", 
                            first=first, 
                            last=last, 
                            github=github,
                            projects=projects)
    return html


# @app.route("/student/<github>")
# def show_student(github):
#     if request.args.get("search"):

#     pass

@app.route("/student-form")
def display_form():
    """Display form for adding student information."""

    return render_template("student_add.html")

@app.route("/display_student_form", methods=['POST'])
def display_form_confirmation():

    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    github = request.form.get("github")

    github = hackbright.make_new_student(first_name, last_name, github)
    # return redirect('/student/%s') % github
    first, last, github = hackbright.get_student_by_github(github)
    html = render_template("student_add_confirmation.html", 
                            first=first, 
                            last=last, 
                            github=github)
    return html

@app.route("/project_search")
def search_project_info():
    """Display project information."""

    return render_template("project_search.html")

@app.route("/project")
def display_project_info():
    """Display project information."""

    title = request.args.get("title")
    project_info = hackbright.get_project_by_title(title)
    student_grades = hackbright.get_grades_by_title(title)

    return render_template("project_info.html", 
                            project_info=project_info, 
                            student_grades=student_grades)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)