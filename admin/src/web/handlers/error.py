from flask import render_template
from dataclasses import dataclass

@dataclass
class Error:
    title: str
    code: int
    message: str
    description: str

def error_not_found(e):
    error = Error(
        title = "Not Found",
        code = 404,
        message = "The requested URL was not found on the server.",
        description = "If you entered the URL manually please check your spelling and try again."
    )
    return render_template("error.html", error = error), 404

def unautorized(e):
    error = Error(
        title = "Unauthorized",
        code = 401,
        message = "You are not authorized to access this page.",
        description = "Please login with the correct credentials."
    )
    return render_template("error.html", error = error), 401