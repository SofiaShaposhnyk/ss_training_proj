from os import environ as env

web = {
    'web_host': env.get('WEB_HOST'),
    'web_port': env.get('WEB_PORT'),
    'debug': False
}

db = {
    'db_user': env.get('DB_USER'),
    'db_password': env.get('DB_PASSWORD'),
    'db_name': env.get('DB_NAME'),
    'db_host': env.get('DB_HOST'),
    'db_port': env.get('DB_PORT')
}

redis = {
    'redis_host': env.get('REDIS_HOST'),
    'redis_port': env.get('REDIS_PORT')
}
