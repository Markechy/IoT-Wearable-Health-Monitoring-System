from flask import Blueprint, render_template, request, flash, redirect, url_for
import mysql.connector
import json

mysql_host = "localhost"
mysql_user = "root"
mysql_password = ""
mysql_database = "retov_1_0"
id=0

views = Blueprint("views", __name__)

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

@views.route("/", methods=["GET", "POST"])
def home():
    global id
    try:
        with open("ar.txt", 'r') as archivo:
            id = int(archivo.read())
            archivo.close()
    except FileNotFoundError:
        id = 0

    if id == 0:
        return redirect(url_for("auth.login"))
    else:
        return render_template("MENU.html")

@views.route("/frec", methods = ["GET", "POST"])
def frec():
    global id
    if request.method == "POST":
        var = request.form.get('period_selector')
        if var == 'semana':
            etiquetas = []
            datos_frec = []
            res = sql_querry(f"SELECT fecha, valor FROM pulso WHERE fecha >= CURDATE() - INTERVAL 7 DAY AND numero_de_serie = {id} ORDER BY fecha DESC;")
            print(res)
            for i in range(len(res)):
                etiquetas.append(str(res[i][0]))
                datos_frec.append(int(res[i][1]))
            return render_template("FREC.html", etiquetas = json.dumps(etiquetas), datos_frec = datos_frec)
        elif var == 'dia':
            etiquetas = []
            datos_frec = []
            res = sql_querry(f"SELECT fecha, valor FROM pulso WHERE fecha >= CURDATE() AND fecha <= NOW() AND numero_de_serie = {id};")
            print(res)
            for i in range(len(res)):
                etiquetas.append(str(res[i][0]))
                datos_frec.append(int(res[i][1]))
            return render_template("FREC.html", etiquetas = json.dumps(etiquetas), datos_frec = datos_frec)
        elif var == 'hora':
            etiquetas = []
            datos_frec = []
            res = sql_querry(f"SELECT fecha, valor FROM pulso WHERE fecha >= NOW() - INTERVAL 60 MINUTE AND numero_de_serie = {id};")
            print(res)
            for i in range(len(res)):
                etiquetas.append(str(res[i][0]))
                datos_frec.append(int(res[i][1]))
            return render_template("FREC.html", etiquetas = json.dumps(etiquetas), datos_frec = datos_frec)
    else:
        etiquetas = []
        datos_frec = []
        res = sql_querry(f"SELECT fecha, valor FROM pulso WHERE fecha >= CURDATE() - INTERVAL 7 DAY AND numero_de_serie = {id} ORDER BY fecha DESC;")
        print(res)
        for i in range(len(res)):
            etiquetas.append(str(res[i][0]))
            datos_frec.append(int(res[i][1]))
        return render_template("FREC.html", etiquetas = json.dumps(etiquetas), datos_frec = datos_frec)

@views.route("/oxig", methods = ["GET", "POST"])
def oxig():
    global id
    if request.method == "POST":
        var = request.form.get('period_selector')
        if var == 'semana':
            etiquetas = []
            datos_oxi = []
            res = sql_querry(f"SELECT fecha, valor FROM oxigenacion WHERE fecha >= CURDATE() - INTERVAL 7 DAY ORDER BY fecha DESC, numero_de_serie = {id};")
            print(res)
            for i in range(len(res)):
                etiquetas.append(str(res[i][0]))
                datos_oxi.append(int(res[i][1]))
            return render_template("OXIG.html", etiquetas = json.dumps(etiquetas), datos_oxi = datos_oxi)
        elif var == 'dia':
            etiquetas = []
            datos_oxi= []
            res = sql_querry(f"SELECT fecha, valor FROM oxigenacion WHERE fecha >= CURDATE() - INTERVAL 7 DAY AND numero_de_serie = {id} ORDER BY fecha DESC;")
            print(res)
            for i in range(len(res)):
                etiquetas.append(str(res[i][0]))
                datos_oxi.append(int(res[i][1]))
            return render_template("OXIG.html", etiquetas = json.dumps(etiquetas), datos_oxi = datos_oxi)
        elif var == 'hora':
            etiquetas = []
            datos_oxi = []
            res = sql_querry(f"SELECT fecha, valor FROM oxigenacion WHERE fecha >= NOW() - INTERVAL 60 MINUTE AND numero_de_serie = {id};")
            print(res)
            for i in range(len(res)):
                etiquetas.append(str(res[i][0]))
                datos_oxi.append(int(res[i][1]))
            return render_template("OXIG.html", etiquetas = json.dumps(etiquetas), datos_oxi = datos_oxi)
    else:
        etiquetas = []
        datos_oxi = []
        res = sql_querry(f"SELECT fecha, valor FROM oxigenacion WHERE fecha >= CURDATE() - INTERVAL 7 DAY AND numero_de_serie = {id} ORDER BY fecha DESC;")
        print(res)
        for i in range(len(res)):
            etiquetas.append(str(res[i][0]))
            datos_oxi.append(int(res[i][1]))
        return render_template("OXIG.html", etiquetas = json.dumps(etiquetas), datos_oxi = datos_oxi)

@views.route("/temp", methods = ["GET", "POST"])
def temp():
    global id
    if request.method == "POST":
        var = request.form.get('period_selector')
        if var == 'semana':
            etiquetas = []
            datos_temp = []
            res = sql_querry(f"SELECT fecha, valor FROM temperatura WHERE fecha >= CURDATE() - INTERVAL 7 DAY ORDER BY fecha DESC, numero_de_serie = {id};")
            print(res)
            for i in range(len(res)):
                etiquetas.append(str(res[i][0]))
                datos_temp.append(int(res[i][1]))
            return render_template("TEMPE.html", etiquetas = json.dumps(etiquetas), datos_temp = datos_temp)
        elif var == 'dia':
            etiquetas = []
            datos_temp= []
            res = sql_querry(f"SELECT fecha, valor FROM temperatura WHERE fecha >= CURDATE() - INTERVAL 7 DAY AND numero_de_serie = {id} ORDER BY fecha DESC;")
            print(res)
            for i in range(len(res)):
                etiquetas.append(str(res[i][0]))
                datos_temp.append(int(res[i][1]))
            return render_template("TEMPE.html", etiquetas = json.dumps(etiquetas), datos_temp = datos_temp)
        elif var == 'hora':
            etiquetas = []
            datos_temp = []
            res = sql_querry(f"SELECT fecha, valor FROM temperatura WHERE fecha >= NOW() - INTERVAL 60 MINUTE AND numero_de_serie = {id};")
            print(res)
            for i in range(len(res)):
                etiquetas.append(str(res[i][0]))
                datos_temp.append(int(res[i][1]))
            return render_template("TEMPE.html", etiquetas = json.dumps(etiquetas), datos_temp = datos_temp)
    else:
        etiquetas = []
        datos_temp = []
        res = sql_querry(f"SELECT fecha, valor FROM temperatura WHERE fecha >= CURDATE() - INTERVAL 7 DAY AND numero_de_serie = {id} ORDER BY fecha DESC;")
        print(res)
        for i in range(len(res)):
            etiquetas.append(str(res[i][0]))
            datos_temp.append(int(res[i][1]))
        return render_template("TEMPE.html", etiquetas = json.dumps(etiquetas), datos_temp = datos_temp)

@views.route("/hum", methods = ["GET", "POST"])
def hum():
    global id
    if request.method == "POST":
        var = request.form.get('period_selector')
        if var == 'semana':
            etiquetas = []
            datos_hum = []
            res = sql_querry(f"SELECT fecha, valor FROM humedad WHERE fecha >= CURDATE() - INTERVAL 7 DAY ORDER BY fecha DESC, numero_de_serie = {id};")
            print(res)
            for i in range(len(res)):
                etiquetas.append(str(res[i][0]))
                datos_hum.append(int(res[i][1]))
            return render_template("HUME.html", etiquetas = json.dumps(etiquetas), datos_hum = datos_hum)
        elif var == 'dia':
            etiquetas = []
            datos_hum= []
            res = sql_querry(f"SELECT fecha, valor FROM humedad WHERE fecha >= CURDATE() - INTERVAL 7 DAY AND numero_de_serie = {id} ORDER BY fecha DESC;")
            print(res)
            for i in range(len(res)):
                etiquetas.append(str(res[i][0]))
                datos_hum.append(int(res[i][1]))
            return render_template("HUME.html", etiquetas = json.dumps(etiquetas), datos_hum = datos_hum)
        elif var == 'hora':
            etiquetas = []
            datos_hum = []
            res = sql_querry(f"SELECT fecha, valor FROM humedad WHERE fecha >= NOW() - INTERVAL 60 MINUTE AND numero_de_serie = {id};")
            print(res)
            for i in range(len(res)):
                etiquetas.append(str(res[i][0]))
                datos_hum.append(int(res[i][1]))
            return render_template("HUME.html", etiquetas = json.dumps(etiquetas), datos_hum = datos_hum)
    else:
        etiquetas = []
        datos_hum = []
        res = sql_querry(f"SELECT fecha, valor FROM humedad WHERE fecha >= CURDATE() - INTERVAL 7 DAY AND numero_de_serie = {id} ORDER BY fecha DESC;")
        print(res)
        for i in range(len(res)):
            etiquetas.append(str(res[i][0]))
            datos_hum.append(int(res[i][1]))
        return render_template("HUME.html", etiquetas = json.dumps(etiquetas), datos_hum = datos_hum)
