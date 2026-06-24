from flask import Blueprint, render_template, request, flash, redirect, url_for
import mysql.connector

mysql_host = "localhost"
mysql_user = "root"
mysql_password = ""
mysql_database = "retov_1_0"

auth = Blueprint("auth", __name__)

def sql_querry(query):
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        print("Datos recuperados de MySQL correctamente")
        return result
    except mysql.connector.Error as error:
        print("Error al conectar a MySQL:", error)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        id = request.form.get("user")
        res = sql_querry(f"select p_nombre from usuario where idUsuario = {id}")
        if len(res) >= 1:
            with open("ar.txt", 'w') as archivo:
                archivo.write(str(id))
                archivo.close()
            return redirect(url_for("views.home"))
    return render_template("LOGIN.html")

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        pn = request.form.get("pnombre")
        sn = request.form.get("snombre")
        pa = request.form.get("papellido")
        sa = request.form.get("sapellido")
        f = request.form.get("fecha")
        t = request.form.get("tel")
        al = request.form.get("altura")
        p = request.form.get("peso")
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )
        cursor = connection.cursor()
        cursor.execute(f"Insert into usuario (p_nombre, s_nombre, p_apellido, s_apellido, fecha_de_nacimiento, telefono, altura, peso) values ('{pn}', '{sn}', '{pa}', '{sa}', '{f}', '{t}', {al}, {p})")
        connection.commit()
        connection.close()
        return redirect(url_for("views.home"))
    return render_template("CREAR.html")
