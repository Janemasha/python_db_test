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

    def __del__(self):
        self.DB_CONNECTION.close()

db_manager = DatabaseManager()
