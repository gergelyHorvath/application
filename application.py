import psycopg2


def main():
    options = {
        '0': list_table, 'q': quit_app, '1': list_mentors, '2': nicks_from_city, '3': find_applicant,
        '4': find_by_mail, '5': add_new_applicant, '6': change_phone_num, '7': delete_applicants
        }
    try:
        connect_str = "dbname='Application' user='postgres' host='localhost' password='mellon'"
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
    except Exception as e:
        print("Unable to connect. Invalid dbname, user or password?")
        print(e)
    entry = 'm'
    while entry != 'q':
        print_menu()
        do_this = ask_for_input()
        options[do_this](cursor)
        entry = input("\n\n Enter 'q' to exit, anything else to return to menu")
    quit_app()


def print_menu():
    print("""
    Please press button to activate feature:

    0 - List full table
    1 - List the names of the mentors
    2 - List the nickname of the mentors from a specific city
    3 - Find an applicant by first name
    4 - Find an applicant by e-mail
    5 - Add a new applicant to database
    6 - Change phone number of an applicant
    7 - Delete applicants
    q - Exit program""")


def ask_for_input():
    to_do = input('\nPlease choose an action:')
    while to_do not in [str(num) for num in range(8)] + ['q']:
        to_do = input('\nPlease enter something from the given options')
    return to_do


def quit_app(q='q'):
    print('\nThank you for using application.py, bye!')
    quit()


def list_table(cursor):
    print("""\nView the full table of
    1 - The mentors
    2 - The applicants""")
    ment_or_app = input('Enter your choice:')
    while ment_or_app not in ('1', '2'):
        ment_or_app = input('1 or 2 please')
    table = 'mentors' if ment_or_app == '1' else 'applicants'
    cursor.execute("""SELECT * FROM {};""".format(table))
    all_info = cursor.fetchall()
    not_so_pretty_print(all_info)


def list_mentors(cursor):
    cursor.execute('SELECT first_name, last_name from mentors')
    mentors = cursor.fetchall()
    not_so_pretty_print(mentors)


def nicks_from_city(cursor):
    cursor.execute('SELECT DISTINCT city from mentors')
    cities = cursor.fetchall()
    print('\n The mentors are from:')
    for i, city in enumerate(cities):
        print('{}- {}'.format(i+1, city[0]))
    city_idx = None
    while city_idx not in [str(num) for num in range(1, len(cities)+1)]:
        city_idx = input('List the nicknames of all the mentors from a city, please enter the appropriate number:')
    city = cities[int(city_idx)-1][0]
    cursor.execute("""SELECT nick_name FROM mentors WHERE city='{}'""".format(city))
    nicks = cursor.fetchall()
    not_so_pretty_print(nicks)


def find_applicant(cursor):
    cursor.execute(
        """SELECT CONCAT (first_name,' ', last_name) AS full_name, phone_number FROM applicants
        WHERE first_name='Carol'"""
    )
    person = cursor.fetchall()
    not_so_pretty_print(person)


def find_by_mail(cursor):
    cursor.execute(
        """SELECT CONCAT (first_name,' ', last_name) AS full_name, phone_number FROM applicants
        WHERE email LIKE'%@adipiscingenimmi.edu'"""
    )
    person = cursor.fetchall()
    not_so_pretty_print(person)


def add_new_applicant(cursor):
    cursor.execute("""SELECT application_code FROM applicants WHERE application_code=54823;""")
    app_code = cursor.fetchall()
    if not app_code:
        cursor.execute(
            """INSERT INTO applicants (first_name, last_name, phone_number, email, application_code)
            VALUES ('Markus', 'Schaffarzyk', '003620/725-2666', 'djnovus@groovecoverage.com', 54823);"""
            )
    else:
        print('\nApplicant (code:54823) is already in database')
    cursor.execute("""SELECT * FROM applicants WHERE application_code=54823;""")
    person = cursor.fetchall()
    not_so_pretty_print(person)


def change_phone_num(cursor):
    cursor.execute(
        """UPDATE applicants
        SET phone_number='003670/223-7459'
        WHERE first_name='Jemima' AND last_name='Foreman';"""
        )
    cursor.execute("""SELECT phone_number from applicants WHERE first_name='Jemima' AND last_name='Foreman';""")
    phone_num = cursor.fetchall()
    not_so_pretty_print(phone_num)


def delete_applicants(cursor):
    cursor.execute("""SELECT * FROM applicants WHERE email LIKE '%@mauriseu.net';""")
    people = cursor.fetchall()
    if people:
        cursor.execute("""DELETE FROM applicants WHERE email LIKE '%@mauriseu.net';""")
        print('Applicants deleted')
    else:
        print('\nThe requested applicants have already been removed from database')


def not_so_pretty_print(data):
    list_of_strings = ['  '.join(map(str, row)) for row in data]
    max_length = len(max(list_of_strings, key=len))
    print('\n' + '-' * max_length)
    for row in list_of_strings:
        print(row)
    print('-' * max_length)


if __name__ == '__main__':
    main()
