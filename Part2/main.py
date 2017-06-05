import data_manager as dm
from flask import Flask, render_template, request, redirect

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
    SELECT a.first_name, a.application_code, COALESCE(m.first_name, 'None yet'), COALESCE(m.last_name, 'None yet')
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
    question = ('List all the:',)
    radio = ['mentors', 'applicants']
    path_to_go = '/full-tables/print'
    return render_template('input.html', question=question, radio=radio, path_to_go=path_to_go)


@app.route('/full-tables/print')
def print_full_tables():
    choice = request.args['radio']
    if choice not in ('mentors', 'applicants'):
        return redirect('/')
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
    question = ('Select a city:',)
    radio = [city[0] for city in cities]
    path_to_go = '/nicks-from-city/print'
    return render_template('input.html', question=question, radio=radio, path_to_go=path_to_go)


@app.route('/nicks-from-city/print')
def print_nicks_from_city():
    choice = request.args['radio']
    sql_query = """
    SELECT nick_name FROM mentors
    WHERE city=%s;"""
    table = dm.run_query(sql_query, (choice,))
    title = 'All the mentors from {}'.format(choice)
    header = ('Nick Name',)
    return render_template('print_table.html', title=title, header=header, table=table)


@app.route('/applicant-by-first-name')
def app_by_fn():
    question = ('Search applicants by first name :',)
    text = ('Carol',)
    path_to_go = '/applicant-by-first-name/print'
    return render_template('input.html', question=question, text=text, path_to_go=path_to_go)


@app.route('/applicant-by-first-name/print')
def print_app_by_fn():
    choice = request.args['input0']
    sql_query = """
    SELECT CONCAT (first_name,' ', last_name) AS full_name, phone_number FROM applicants
    WHERE first_name ILIKE %s;"""
    table = dm.run_query(sql_query, ('%' + choice + '%',))
    title = 'Applicants with the first name: {}'.format(choice)
    header = ('Name', 'Phone Number')
    return render_template('print_table.html', title=title, header=header, table=table)


@app.route('/applicant-by-email')
def app_by_mail():
    question = ('Search applicants by eMail :',)
    text = ('@adipiscingenimmi.edu',)
    path_to_go = '/applicant-by-email/print'
    return render_template('input.html', question=question, text=text, path_to_go=path_to_go)


@app.route('/applicant-by-email/print')
def print_app_by_mail():
    choice = request.args['input0']
    sql_query = """
    SELECT CONCAT (first_name,' ', last_name) AS full_name, phone_number FROM applicants
    WHERE email ILIKE %s;"""
    table = dm.run_query(sql_query, ('%' + choice + '%',))
    title = 'Applicants with their email address containing {}'.format(choice)
    header = ('Name', 'Phone Number')
    return render_template('print_table.html', title=title, header=header, table=table)


@app.route('/add-new-applicant')
def add_new_applicant():
    question = ('First Name:', 'Last Name:', 'Phone Number:', 'Email Address:', 'Application Code:')
    text = ('Markus', 'Schaffarzyk', '003620/725-2666', 'djnovus@groovecoverage.com', 54823)
    path_to_go = '/add-new-applicant/commit'
    return render_template('input.html', question=question, text=text, path_to_go=path_to_go)


@app.route('/add-new-applicant/commit')
def save_new_applicant():
    choice = [_input for _input in request.args.values()]
    try:
        choice[-1] = int(choice[-1])
    except ValueError:
        message = 'The application code must be an integer!'
        return render_template('errors.html', message=message)
    app_codes = [code[0] for code in dm.run_query("SELECT application_code FROM applicants")]
    if choice[-1] in app_codes:
        message = 'There already is an applicant with the application code: {}'.format(choice[-1])
        return render_template('errors.html', message=message)
    choice = tuple(choice)
    sql_query = """
    INSERT INTO applicants (first_name, last_name, phone_number, email, application_code)
    VALUES (%s, %s, %s, %s, %s);"""
    dm.run_query(sql_query, variables=choice, with_reurnvalue=False)
    return redirect('/full-tables/print?radio=applicants')


@app.route('/delete-applicant')
def delete_applicant():
    question = ('Enter application code to delete applicant:',)
    text = ('',)
    path_to_go = '/delete-applicant/commit'
    return render_template('input.html', question=question, text=text, path_to_go=path_to_go)


@app.route('/delete-applicant/commit')
def delete_applicant_from_db():
    try:
        choice = int(request.args['input0'])
    except ValueError:
        message = 'The application code must be an integer!'
        return render_template('errors.html', message=message)
    app_codes = [code[0] for code in dm.run_query("SELECT application_code FROM applicants")]
    if choice not in app_codes:
        message = 'There is no applicant in the database with the application code: {}'.format(choice)
        return render_template('errors.html', message=message)
    sql_query = """
    DELETE FROM applicants
    WHERE application_code = %s;"""
    dm.run_query(sql_query, variables=(choice,), with_reurnvalue=False)
    return redirect('/full-tables/print?radio=applicants')


if __name__ == '__main__':
    app.run(debug=True)
