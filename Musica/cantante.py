from flask import Blueprint, app, render_template

from . import db


bp = Blueprint('cantante',__name__,url_prefix='/cantante') 

@bp.route('/')
def lista():
    base_de_datos = db.get_db()
    consulta = """
         SELECT Name, ArtistId FROM artists
         ORDER BY Name ASC
    """
    con = db.get_db()
    res = con.execute(consulta)
    lista_de_cantantes = res.fetchall()
    pagina = render_template('cantantes.html', cantantes=lista_de_cantantes)

    return render_template("cantantes.html", cantantes=lista_de_cantantes) 

@bp.route('/<int:id>')
def detalle(id):
    con = db.get_db()
    consulta1 = """
            SELECT name, ArtistId FROM artists WHERE ArtistId = ?
"""
    consulta2 = """
    SELECT al.Title FROM artists a JOIN albums al ON a.ArtistId = al.ArtistId
    WHERE a.ArtistId = ?;
"""

    res = con.execute(consulta1,(id,))
    cantante = res.fetchone()
    res = con.execute(consulta2, (id,))
    lista_de_albums = res.fetchall()

    pagina = render_template('detalle_cantante.html',
                             cantante=cantante,
                             albums = lista_de_albums)
    return pagina