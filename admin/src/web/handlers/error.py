from dataclasses import dataclass
from flask import render_template

@dataclass
class Error:
    code: int
    message: str
    description: str

def error_not_found(e):
    error = Error(404, "Not Found", "La URL solicitada no se encontró en el servidor.")
    return render_template("error.html", error = error), 404