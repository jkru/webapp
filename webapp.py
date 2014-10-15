from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row1 = hackbright_app.get_student_by_github(student_github)
    row2 = hackbright_app.query_grades_by_student(row1[1])
    print "********************************************"
    print "this is row 2", row2
    print "********************************************"

    get_grades = []
    get_project = []
    for i in range(len(row2)):
        get_project.append(row2[i][0])
        get_grades.append(row2[i][1])

    html = render_template("student_info.html", first_name=row1[0], last_name=row1[1], github=row1[2], projects = get_project, grades=get_grades)
    return html

@app.route("/project_grades")
def grades_by_project():
    hackbright_app.connect_to_db()
    



if __name__ == "__main__":
    app.run(debug=True)

