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

if __name__ == '__main__':
    app.run(debug=True)
