import sqlite3

DB = None
CONN = None

def help_function():
    print ("Student: Query by github name.")
    print ("Usage: HBA> student <github>")
    print ("New Student: add new student.")
    print ("Usage: HBA> new_student <first_name> <last_name> <github>")
    print ("Project: Query by project title.")
    print ("Usage: HBA> project_title <project>")
    print ("New Project: Create a new project.")
    print ("Usage: HBA> new_project <title> <description> <max_grade>")
    print ("Grade By Project: All grades for given project")
    print ("Usage: HBA> grade_project_query <title>")
    print ("Give Grade: enter new grade for new project")
    print ("Usage: HBA> give_grade <github> <project title> <grade>")
    print ("Display Grade: Show grades for given student")
    print ("Usage: HBA> display_grade <last_name>")
    print ("Help: show help function")
    print ("Usage: HBA> help")

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    try:
        DB.execute(query, (github,))
        row = DB.fetchone()
        print """\
    Student: %s %s
    Github account: %s"""%(row[0], row[1], row[2])
    except:
        print "entry not found"

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?,?,?)"""
    DB.execute(query,(first_name,last_name,github))
    CONN.commit()
    print "Successfully added student: %s %s"%(first_name,last_name)

def query_projects_by_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    try:
        DB.execute(query,(title,))
        row = DB.fetchone()
        print """\
        Title: %s 
        Description: %s
        Score: %d"""%(row[1], row[2], row[3])
    except:
        print "entry not found"

def query_grades_by_project_title(title):
    query = """SELECT grade, Students.last_name FROM grades
               JOIN Students ON (student_github=github)
               WHERE project_title=?
            """
    try:
        DB.execute(query,(title,))
        row = DB.fetchone()
        print """\
        Student: %s
        Grade: %s"""%(row[1], row[0])
    except:
        print "entry not found"

def query_grades_by_student(last_name):
    query = """SELECT project_title, grade FROM grades
               JOIN Students ON (student_github=github)
               WHERE last_name=?
            """
    try:
        DB.execute(query,(last_name,))
        print
        row = DB.fetchone()
        print """\
        Project: %s
        Grade: %s"""%(row[0],row[1])
    except:
        print "entry not found"

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) VALUES (?,?,?)"""
    DB.execute(query,(title,description,max_grade))
    CONN.commit()
    print "Successfully added project: %s"% title

def give_grade(student_github, project_title, grade):
    query = """INSERT INTO Grades (student_github, project_title, grade) 
            VALUES (?,?,?)""" 
    DB.execute(query,(student_github, project_title, grade,))
    CONN.commit()
    print "Successfully added grade to: %s"% student_github




def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            try:
                get_student_by_github(*args)
            except:
                print "Incorrect number of arguments. Type 'help' for info."
        elif command == "new_student":
            try:
                make_new_student(*args)
            except:
                print "Incorrect number of arguments. Type 'help' for info."
        elif command == "project_title":
            try: 
                query_projects_by_title(*args)
            except:
                print "Incorrect number of arguments. Type 'help' for info."
        elif command == "new_project":
            try: 
                make_new_project(*args)
            except:
                print "Incorrect number of arguments. Type 'help' for info."
        elif command == "grade_project_query":
            try:
                query_grades_by_project_title(*args)
            except:
                print "Incorrect number of arguments. Type 'help' for info."
        elif command == "give_grade":
            try:
                give_grade(*args)
            except:
                print "Incorrect number of arguments. Type 'help' for info."
        elif command == "display_grade":
            try:
                query_grades_by_student(*args)
            except:
                print "Incorrect number of arguments. Type 'help' for info."
        elif command == "help" or command == "Help":
            help_function()
        else:
            print "Not a real command."
            help_function()
            

    CONN.close()

if __name__ == "__main__":
    main()
