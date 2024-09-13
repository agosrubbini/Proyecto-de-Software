from flask import render_template

error = {
    "title": "Ups, algo salió mal...",
    "code": 404,
    "message": "Not Found",
    "description": "La URL solicitada no se encontró en el servidor."
}

def error_not_found(e):
    return render_template("error.html", error = error), 404