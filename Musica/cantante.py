from flask import Flask, render_template
from . import bp


bp = Blueprint('cantante',__name__, url_prefix='/cantantes')

@bp.route('/cantantes')
def cantantes():
    consulta = """
    SELECT first_name, last_name, artistsId FROM cantante
    ORDER BY last_name, first_name;
    """
    con = db.get_db()
    res = con.execute(consulta)
    lista_cantantes = res.fetchall()
    pagina = render_template('cantantes.html', cantantes=lista_cantantes)
    return pagina

@bp.route('/<init:id>')
def detalle(id):
    con = db.get_db()
    consulta1 = """
        SELECT first_name, last_name FROM cantante WHERE artistsId =?;
    """
    consulta2 = """
     SELECT title FROM cantante c JOIN 
    """

    res = con.execute(consulta1, (id,))
    cantante = res.fetchone()
    res = con.execute(consulta2, (id,))
    lista_canciones = res.fetchall()

    pagina = render_template('detalle_cantantes.html',
                             cantante=cantante,
                             canciones=lista_canciones)
    return pagina