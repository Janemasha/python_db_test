import psycopg2

class DatabaseManager:

    def __init__(self):
        self.DB_CONNECTION = psycopg2.connect(
            dbname='animal_shelter',
            user='postgres',
            password='postgres',
            host='localhost',
            port=5432
        )
        self.DB_CURSOR = self.DB_CONNECTION.cursor()
        self.__create_db_tables()


    def __create_db_tables(self):

        create_employee_table_query = """
            CREATE TABLE IF NOT EXISTS employee(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(200),
                last_name VARCHAR(200),
                position VARCHAR(200)
            );
        """

        create_pets_type_table_query = """
            CREATE TABLE IF NOT EXISTS pets_type(
                id SERIAL PRIMARY KEY,
                name VARCHAR(200)
            );
        """

        create_client_table_query = """
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(200),
                last_name VARCHAR(200),
                mobile_phone VARCHAR(100)
            );
        """

        create_pet_table_query = """
            CREATE TABLE IF NOT EXISTS pet(
                id SERIAL PRIMARY KEY,
                name VARCHAR(200),
                type_id INTEGER REFERENCES pets_type(id),
                client_id INTEGER REFERENCES client(id)
            );
        """

        create_pet_connection_table_query = """
            CREATE TABLE IF NOT EXISTS pet_connection(
                id SERIAL PRIMARY KEY,
                pet_id INTEGER REFERENCES pet(id),
                employee_id INTEGER REFERENCES employee(id)
            );            
        """
        self.DB_CURSOR.execute(create_employee_table_query)
        self.DB_CURSOR.execute(create_pets_type_table_query)
        self.DB_CURSOR.execute(create_client_table_query)
        self.DB_CURSOR.execute(create_pet_table_query)
        self.DB_CURSOR.execute(create_pet_connection_table_query)
        self.DB_CONNECTION.commit()


    def add_employee(self):
        is_right_employee = False
        while not is_right_employee:
            employee_first_name = input('Enter first name of employee: ')
            employee_last_name = input('Enter last name of employee: ')
            employee_position = input('Enter position of employee: ')
            if employee_position.isalpha() and employee_first_name.isalpha() and employee_last_name.isalpha():
                add_employee_query = """
                    INSERT INTO employee (first_name, last_name, position) values (%s, %s, %s);
                """
                self.DB_CURSOR.execute(add_employee_query, (employee_first_name, employee_last_name, employee_position))
                self.DB_CONNECTION.commit()
                is_right_employee = True
            else:
                print('First name, last name and position must contain only letters')


    def add_pets_type(self):
        is_right_pets_type = False
        while not is_right_pets_type:
            pets_type_name = input('Enter name of pets type: ')
            if pets_type_name.isalpha():
                add_pets_type_query = """
                    INSERT INTO pets_type (name) values (%s);
                """
                self.DB_CURSOR.execute(add_pets_type_query, (pets_type_name, ))
                self.DB_CONNECTION.commit()
                is_right_pets_type = True
            else:
                print('Name of pets type must contain only letters')


    def add_client(self):
        is_right_client = False
        while not is_right_client:
            client_first_name = input('Enter first name of client: ')
            client_last_name = input('Enter last name of client: ')
            client_phone = input('Enter phone of client (just numbers): ')
            if client_first_name.isalpha() and client_last_name.isalpha():
                if client_phone.isdigit():
                    add_client_query = """
                        INSERT INTO client (first_name, last_name, mobile_phone) values (%s, %s, %s);
                    """
                    self.DB_CURSOR.execute(add_client_query, (client_first_name, client_last_name, client_phone))
                    self.DB_CONNECTION.commit()
                    is_right_client = True
                else:
                    print('Mobile phone must contain numbers only')
            else:
                print('First name, last name must contain only letters')


    def add_pet(self):
        is_right_pet_name = False
        pet_name = None
        while not is_right_pet_name:
            new_pet_name = input('Enter name of pets type: ')
            if new_pet_name.isalpha():
                pet_name = new_pet_name
                is_right_pet_name = True
            else:
                print('Name of pet must contain only letters')

        is_right_type = False
        type_id = None
        while not is_right_type:
            pet_type = input('Enter number of pets type: ')
            if pet_type.isdigit():
                pet_type_id = int(pet_type)
                is_right_id = self.find_pet_type_by_id(pet_type_id)
                if is_right_id:
                    is_right_type = True
                    type_id = pet_type_id
                else:
                    print('Number of pets type is wrong')
            else:
                print('Number of pets type is wrong')

        is_right_client = False
        client_id = None
        while not is_right_client:
            pet_client = input('Enter number of client: ')
            if pet_client.isdigit():
                pet_client_id = int(pet_client)
                is_right_id = self.find_client_by_id(pet_client_id)
                if is_right_id:
                    is_right_client = True
                    client_id = pet_client_id
                else:
                    print('Number of client is wrong')
            else:
                print('Number of client is wrong')

        add_pet_query = """
                        INSERT INTO pet (name, type_id, client_id) values (%s, %s, %s);
                    """
        self.DB_CURSOR.execute(add_pet_query, (pet_name, type_id, client_id))
        self.DB_CONNECTION.commit()


    def find_client_by_id(self, client_id):
        client_query = """
                    SELECT id FROM client;
                """
        self.DB_CURSOR.execute(client_query)
        result = self.DB_CURSOR.fetchall()
        is_right_id = False
        if len(result) != 0:
            for item in result:
                if item[0] == client_id:
                    is_right_id = True
        return is_right_id


    def find_pet_type_by_id(self, pet_type_id):
        type_query = """
                    SELECT id FROM pets_type;
                """
        self.DB_CURSOR.execute(type_query)
        result = self.DB_CURSOR.fetchall()
        is_right_id = False
        if len(result) != 0:
            for item in result:
                if item[0] == pet_type_id:
                    is_right_id = True
        return is_right_id


    def add_pet_connection(self):
        is_right_pet = False
        pet_id = None
        while not is_right_pet:
            user_pet_id = input('Enter number of pet: ')
            if user_pet_id.isdigit():
                new_pet_id = int(user_pet_id)
                is_right_id = self.find_pet_by_id(new_pet_id)
                if is_right_id:
                    is_right_pet = True
                    pet_id = new_pet_id
                else:
                    print('Number of pet is wrong')
            else:
                print('Number of pet is wrong')

        is_right_employee = False
        employee_id = None
        while not is_right_employee:
            pet_employee = input('Enter number of client: ')
            if pet_employee.isdigit():
                pet_employee_id = int(pet_employee)
                is_right_id = self.find_employee_by_id(pet_employee_id)
                if is_right_id:
                    is_right_employee = True
                    employee_id = pet_employee_id
                else:
                    print('Number of employee is wrong')
            else:
                print('Number of employee is wrong')

        add_pet_query = """
                        INSERT INTO pet_connection (employee_id, pet_id) values (%s, %s);
                    """
        self.DB_CURSOR.execute(add_pet_query, (employee_id, pet_id))
        self.DB_CONNECTION.commit()

    def find_pet_by_id(self, pets_id):
        pet_query = """
                    SELECT id FROM pet;
                """
        self.DB_CURSOR.execute(pet_query)
        result = self.DB_CURSOR.fetchall()
        is_right_id = False
        if len(result) != 0:
            for item in result:
                if item[0] == pets_id:
                    is_right_id = True
        return is_right_id

    def find_employee_by_id(self, employee_id):
        employee_query = """
                    SELECT id FROM employee;
                """
        self.DB_CURSOR.execute(employee_query)
        result = self.DB_CURSOR.fetchall()
        is_right_id = False
        if len(result) != 0:
            for item in result:
                if item[0] == employee_id:
                    is_right_id = True
        return is_right_id


    def __del__(self):
        self.DB_CONNECTION.close()



db_manager = DatabaseManager()
db_manager.find_client_by_id(1)


is_right_choice = False
while not is_right_choice:
    user_choice = input('Choose what you want to do:\n'
                        '1 - add new employee,\n'
                        '2 - add new client,\n'
                        '3 - add new pet\n,'
                        '4 - add new type of pet\n'
                        '5 - add connection between pets and employees\n'
                        '6 - close program')

    if user_choice == '1':
        db_manager.add_employee()
        is_right_choice = True
    elif user_choice == '2':
        db_manager.add_client()
        is_right_choice = True
    elif user_choice == '4':
        db_manager.add_pets_type()
        is_right_choice = True
    elif user_choice == '3':
        db_manager.add_pet()
        is_right_choice = True
    elif user_choice == '5':
        db_manager.add_pet_connection()
        is_right_choice = True
    elif user_choice == '6':
        is_right_choice = True
    else:
        print('Wrong choice, try again')