import sqlite3


class Database:
    def __init__(self, path_to_db='static/orders/orders.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_orders(self):
        try:
            sql = """
            CREATE TABLE orders_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name varchar(255) NOT NULL,
            order_name varchar(255) NOT NULL,
            smoke_strength_choice varchar(255) NOT NULL,
            taste_choice varchar(255) NOT NULL,
            second_taste_choice varchar(255) NOT NULL,
            third_taste_choice varchar(255) NOT NULL,
            chatID varchar(255) NOT NULL,
            sqltime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            ); 
            """
            self.execute(sql, commit=True)
        except Exception as e:
            print(e, "in create_table_orders")
            pass

    def add_order(self, name: str, order_name: str, smoke_strength_choice: str, taste_choice: str,
                  second_taste_choice: str, third_taste_choice: str, chatID: str):
        sql = """
        INSERT INTO

        orders_table(name, order_name, smoke_strength_choice, 
                    taste_choice, second_taste_choice, third_taste_choice, chatID) 

        VALUES(?, ?, ?, ?, ?, ?, ?);
        """
        parameters = (name, order_name, smoke_strength_choice, taste_choice,
                      second_taste_choice, third_taste_choice, chatID)
        self.execute(sql, parameters=parameters, commit=True)

    def create_table_old_orders(self):
        try:
            sql = """
            CREATE TABLE create_table_old_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id varchar(255) NOT NULL,
            name varchar(255) NOT NULL,
            order_name varchar(255) NOT NULL,
            smoke_strength_choice varchar(255) NOT NULL,
            taste_choice varchar(255) NOT NULL,
            second_taste_choice varchar(255) NOT NULL,
            third_taste_choice varchar(255) NOT NULL,
            confirmed BOOLEAN NOT NULL,
            deleted BOOLEAN NOT NULL
            ); 
            """
            self.execute(sql, commit=True)
        except Exception as e:
            print(e, "in create_table_old_orders")
            pass

    def add_old_order(self, order_id: str, name: str, order_name: str, smoke_strength_choice: str, taste_choice: str,
                      second_taste_choice: str, third_taste_choice: str, confirmed: bool, deleted: bool):
        sql = """
        INSERT INTO

        create_table_old_orders(order_id, name, order_name, smoke_strength_choice, taste_choice, second_taste_choice, 
        third_taste_choice,
        confirmed, deleted) 

        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        parameters = (order_id, name, order_name, smoke_strength_choice, taste_choice, second_taste_choice,
                      third_taste_choice, confirmed, deleted)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_orders(self, table_name: str):
        sql = f"SELECT * FROM {table_name};"
        return self.execute(sql, fetchall=True)

    def insert_into(self, column, value):
        column, value = str(column), str(value)
        sql = f"INSERT INTO orders_table ({column}) VALUES (?)"
        parameters = (value,)
        self.execute(sql, parameters, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def select_order(self, **kwargs):
        sql = f"SELECT * FROM orders_table WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def count_orders(self):
        return self.execute("SELECT COUNT(*) FROM orders_table;", fetchone=True)

    def delete_order(self, id: int, table):
        sql = f"DELETE FROM {table} WHERE id={id};"
        print(f'order id: {id} was deleted from {table}')
        return self.execute(sql, commit=True)


def logger(statement):
    print(f"""
    _____________________________________________
    Executing:
    {statement}
    _____________________________________________
    """)
