from flask import Blueprint, request, flash, session
from flask import render_template, redirect, url_for
from src.core.horses.models.horse import Horse
from src.core.database import db
from src.core.horses.forms import create_horse_Form
from flask import current_app as app
from src.core.horses.__init__ import create_horse
from sqlalchemy import desc


bp = Blueprint('horses', __name__, url_prefix='/horses')

@bp.route('/')
def list_horses():
    horses = None
    horses = Horse.query.order_by(Horse.name).all()
    context = {
        'horses': horses,
    }
    return render_template('ecuestre/horses.html', context=context)

@bp.route('/create', methods=['GET', 'POST'])
def create_horse_view():
    form = create_horse_Form()
    app.logger.info("El formulario de creación de caballo ha sido enviado: %s", form.validate_on_submit())

    if form.validate_on_submit():
        try:
            # Crear el caballo en la base de datos usando la función importada
            new_horse = create_horse(
                name=form.name.data,
                date_of_birth=form.date_of_birth.data,
                gender=form.gender.data,
                race=form.race.data,
                fur=form.fur.data,
                purchase_or_donation=form.purchase_or_donation.data,
                date_of_entry=form.date_of_entry.data,
                sede=form.sede.data,
                type_jya_assigned=form.type_jya_assigned.data,
                employees=form.employees.data
            )
            
            app.logger.info("Caballo creado exitosamente: %s", form.name.data)#controlar
            flash("Caballo creado exitosamente", "success")
            return redirect(url_for('horses.list_horses'))  # Redirigir a la lista de caballos

        except Exception as e:
            app.logger.error("Error al crear el caballo: %s", str(e))
            flash("Ocurrió un error al crear el caballo", "error")
    context = {
        'form': form,  # Pasa el formulario para que esté disponible en la plantilla
        'horses': Horse.query.order_by(Horse.name).all()  # Puedes cargar los caballos aquí si deseas
    }

    return render_template('ecuestre/create_horse.html', context=context)  # Renderizar el formulario


@bp.route('/order', methods=['POST'])
def order_by():
    order_by = request.form.get('order_option')
    horses = None
    if order_by == 'name_asc':
        horses = Horse.query.order_by(Horse.name).all()
    elif order_by == 'name_desc':
        horses = Horse.query.order_by(desc(Horse.name)).all()
    if order_by == 'birth_date_asc':
        horses = Horse.query.order_by(Horse.date_of_birth).all()
    elif order_by == 'birth_date_desc':
        horses = Horse.query.order_by(desc(Horse.date_of_birth)).all()
    if order_by == 'entry_date_asc':
        horses = Horse.query.order_by(Horse.date_of_entry).all()
    elif order_by == 'entry_date_desc':
        horses = Horse.query.order_by(desc(Horse.date_of_entry)).all()
    context = {
        'horses': horses,
    }
    return render_template('ecuestre/horses.html', context=context)

#actualizar
#eliminar
#asociar entrenadores y conductores
#busqueda