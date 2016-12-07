from orator import DatabaseManager

config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'hedwig',
        'user': 'root',
        'password': 'masukaja',
        'prefix': '',
        'log_queries': True
    }
}

db = DatabaseManager(config)
