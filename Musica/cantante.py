from flask import Blueprint, app, redirect, render_template, request, url_for

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

    return pagina 

@bp.route('/<int:id>')
def detalle(id):
    con = db.get_db()
    consulta1 = """
            SELECT name, ArtistId FROM artists WHERE ArtistId = ?
        """
    consulta2 = """
    SELECT al.Title, a.ArtistId FROM artists a JOIN albums al ON a.ArtistId = al.ArtistId
    WHERE a.ArtistId = ?;
    """

    res = con.execute(consulta1,(id,))
    cantante = res.fetchone()
    res = con.execute(consulta2, (id,))
    lista_de_albums = res.fetchall()

    pagina = render_template('detalle_cantante.html',
                             artista =cantante,
                             albums = lista_de_albums)
    return pagina 

@bp.route("/new", methods=("GET", "POST"))
def nuevo():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]

        con = db.get_db()
        consulta = """ INSERT INTO cantante(firts_name, last_name)
                       VALUES (?, ?) 
                   """
        con.execute(consulta, (first_name, last_name))
        con.commit()
        return redirect(url_for('cantante.cantantes'))
    else:
        pagina = render_template('nuevo_cantante.html')
        return pagina
        
