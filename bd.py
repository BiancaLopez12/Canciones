import os
import sqlite3

import click
from flask import current_app, g

db_folder = current_app.instance.path
db_name = 'spotify.sqlite'
db_file = os.path.join(db_folder, db_name)
db_sql_file = 'discos.sql'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            db_file,
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    # ensure the instance folder exists
    try:
        os.makedirs(current_app.instance_path)
    except OSError:
        pass

    db = get_db()

    with current_app.open_resource(db_sql_file) as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@app.route('/autor')
def actores():
    base_de_datos = db.get_db()
    consulta = """
            SELECT las_name, first FROM actor 
       """
    
    
    resultado = base_de_datos.execute(consulta)
    lista_de_resultados = resultado.fetchall()
    return render_template("actores.html", actores=lista_de_resultados)