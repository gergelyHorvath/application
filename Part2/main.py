import data_manager as dm
from flask import Flask, render_template

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


if __name__ == '__main__':
    app.run(debug=True)
