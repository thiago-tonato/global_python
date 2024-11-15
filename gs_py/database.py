import oracledb

class Database:
    def __init__(self):
        credentials = self.load_credentials("credenciais.txt")
        dsn = f"{credentials['host']}:{credentials['port']}/{credentials['sid']}"

        self.connection = oracledb.connect(
            user=credentials["user"],
            password=credentials["password"],
            dsn=dsn
        )
        self.cursor = self.connection.cursor()

    def load_credentials(self, file_path):
        credentials = {}
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                credentials[key] = value
        return credentials

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or [])
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or [])
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
