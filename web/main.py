from Pagina import create_app

#Manda a llamar a la funcion que crea la aplicación
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
