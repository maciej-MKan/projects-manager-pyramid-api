from pyramid.config import Configurator

# import os
# from dotenv import load_dotenv
#
# load_dotenv('.env/test/db.env')
#
#
# def main(global_config, **settings):
#     config = Configurator(settings=settings)
#     config.include('pyramid_sqlalchemy')
#
#     # Use values from db.env for database connection
#     db_uri = f"postgresql://{os.environ['POSTGRES_USER']}:" \
#              f"{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:" \
#              f"{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
#     config.registry.settings['sqlalchemy.url'] = db_uri
#
#     config.scan()
#
#     return config.make_wsgi_app()