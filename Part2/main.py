import data_manager as dm
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mentors')
def mentors():
    sql_query = """
    SELECT m.first_name, m.last_name, s.name, s.country
        FROM mentors m JOIN schools s
        ON (m.city = s.city)
    ORDER BY m.id;"""
    table = dm.run_query(sql_query)
    title = "Mentors and schools page"
    header = ('First Name', 'Last Name', 'School Name', 'Country')
    return render_template('print_table.html', title=title, header=header, table=table)


@app.route('/all-school')
def all_school():
    sql_query = """
    SELECT m.first_name, m.last_name, s.name, s.country
        FROM mentors m RIGHT OUTER JOIN schools s
        ON (m.city = s.city)
    ORDER BY m.id;"""
    table = dm.run_query(sql_query)
    title = "All the schools page"
    header = ('First Name', 'Last Name', 'School Name', 'Country')
    return render_template('print_table.html', title=title, header=header, table=table)


@app.route('/mentors-by-country')
def mentors_by_country():
    sql_query = """
    SELECT s.country, COUNT(*) AS mentor_count
        FROM mentors m JOIN schools s
        ON (m.city = s.city)
    GROUP BY s.country
    ORDER BY s.country;"""
    table = dm.run_query(sql_query)
    title = 'Mentors by country page'
    header = ('Country', 'Mentor Count')
    return render_template('print_table.html', title=title, header=header, table=table)


@app.route('/contacts')
def contacts():
    sql_query = """
    SELECT s.name, m.first_name, m.last_name
        FROM schools s LEFT OUTER JOIN mentors m
        ON (s.contact_person = m.id)
    ORDER BY s.name;"""
    table = dm.run_query(sql_query)
    title = 'Contacts page'
    header = ('School', 'Contact First Name', 'Last Name')
    return render_template('print_table.html', title=title, header=header, table=table)


@app.route('/applicants')
def applicants():
    sql_query = """
    SELECT a.first_name, a.application_code, a_m.creation_date
        FROM applicants a LEFT OUTER JOIN applicants_mentors a_m
        ON (a.id = a_m.applicant_id)
    WHERE a_m.creation_date > '2016-01-01'
    ORDER BY a_m.creation_date DESC;"""
    table = dm.run_query(sql_query)
    title = 'Applicants page'
    header = ('Applicant First Name', 'Application Code', 'Creation Date')
    return render_template('print_table.html', title=title, header=header, table=table)


@app.route('/applicants-and-mentors')
def applicants_and_mentors():
    sql_query = """
    SELECT a.first_name, a.application_code, COALESCE(m.first_name, 'No mentor yet'), COALESCE(m.last_name, 'No mentor yet')
        FROM ((applicants a LEFT OUTER JOIN applicants_mentors a_m
        ON (a.id = a_m.applicant_id))
            LEFT OUTER JOIN mentors m
            ON (a_m.mentor_id = m.id))
    ORDER BY a_m.applicant_id;"""
    table = dm.run_query(sql_query)
    title = 'Applicants and mentors page'
    header = ('Applicant First Name', 'Application Code', 'Mentor First Name', 'Last Name')
    return render_template('print_table.html', title=title, header=header, table=table)


# Queries from the previous assignment


@app.route('/full-tables')
def full_tables():
    question = 'List all the:'
    radio = ['mentors', 'applicants']
    path_to_go = '/full-tables/print' 
    return render_template('input.html', question=question, radio=radio, path_to_go=path_to_go)


@app.route('/full-tables/print')
def print_full_tables():
    choice = request.args['radio']
    sql_query = """
    SELECT * FROM {};""".format(choice)
    table = dm.run_query(sql_query)
    title = 'List all the {}'.format(choice)
    if choice == 'mentors':
        header = ('ID', 'First Name', 'Last Name', 'Nick', 'Phone number', 'eMail', 'City', 'Favourite Number')
    else:
        header = ('ID', 'First Name', 'Last Name', 'Phone number', 'eMail', 'Application Code')
    return render_template('print_table.html', title=title, header=header, table=table)


@app.route('/nicks-from-city')
def nicks_from_city():
    cities = dm.run_query("SELECT DISTINCT city FROM mentors;")
    question = 'Select a city:'
    radio = [city[0] for city in cities]
    path_to_go = '/nicks-from-city/print'
    return render_template('input.html', question=question, radio=radio, path_to_go=path_to_go)


@app.route('/nicks-from-city/print')
def print_nicks_from_city():
    choice = request.args['radio']
    sql_query = """
    SELECT nick_name FROM mentors
    WHERE city='{}'""".format(choice)
    table = dm.run_query(sql_query)
    title = 'All the mentors from {}'.format(choice)
    header = ('Nick Name',)
    return render_template('print_table.html', title=title, header=header, table=table)

if __name__ == '__main__':
    app.run(debug=True)
