from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.auth.models.user import User
from src.core.auth.models.roles_and_permissions import Role, Permision

def list_users():

    """
        Lista todos los usuarios almacenados en la base de datos y los retorna
    """

    users = User.query.all()

    return users

def create_user(**kwargs):

    """
        Crea un objeto User en la base de datos con los valores recibidos por parámetro
    """

    hash = bcrypt.generate_password_hash(kwargs['password'].encode('utf-8'))
    kwargs['password'] = hash.decode('utf-8')
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def edit_user(**kwargs):

    """
        Edita un objeto User con los valores recibidos por parámetro
    """
    user = kwargs['user']
    hash = bcrypt.generate_password_hash(kwargs['password'].encode('utf-8'))
    user.email = kwargs['email']
    user.alias = kwargs['alias']
    user.active = kwargs['active']
    user.password = hash.decode('utf-8')
    user.role_id = kwargs['role_id']
    db.session.commit()

    return user

def create_role(**kwargs):

    """
        Crea un objeto Role en la base de datos con los valores recibidos por parámetro
    """

    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()

    return role

def create_permission(**kwargs):
    permission = Permision(**kwargs)
    db.session.add(permission)
    db.session.commit()

    return permission

def assign_user(user, role):
    user.role = role
    db.session.add(user)
    db.session.commit()

    return user

def find_user_by_email(email):

    """Devuelve al usuario con el email pasado por parámetro"""

    return User.query.filter_by(email=email).first()


def find_user_by_id(id):

    """Devuelve al usuario con el email pasado por parámetro"""

    return User.query.filter_by(id=id).first()


def find_user_by_alias(alias):

    """Devuelve al usuario con el email pasado por parámetro"""

    return User.query.filter_by(alias=alias).first()

def find_role_id_by_name(name):

    """Devuelve el id del rol con el nombre pasado por parámetro"""

    return Role.query.filter_by(name=name).first().id


def initialice_admin_permissions():
    admin_role = Role.query.filter_by(name="Administración").first()

    # Lista de permisos para el rol Administración
    admin_permissions = [
        "team_index", "team_new", "team_show", "team_update", "team_destroy",
        "payment_index", "payment_new", "payment_show", "payment_update", "payment_destroy",
        "jya_index", "jya_new", "jya_show", "jya_update", "jya_destroy",
        "billing_index", "billing_new", "billing_show", "billing_update", "billing_destroy",
        "horse_index", "horse_show"
    ]

    for perm_name in admin_permissions:
        permission = Permision.query.filter_by(name=perm_name).first()
        if permission:
            admin_role.permissions.append(permission)

    db.session.commit()

def initialice_tecnica_permissions():
    tecnica_role = Role.query.filter_by(name="Técnica").first()

    # Lista de permisos para el rol Técnica
    tecnica_permissions = [
        "jya_index", "jya_new", "jya_show", "jya_update", "jya_destroy",
        "billing_index", "billing_show",
        "horse_index", "horse_show"
    ]

    for perm_name in tecnica_permissions:
        permission = Permision.query.filter_by(name=perm_name).first()
        if permission:
            tecnica_role.permissions.append(permission)

    db.session.commit()


def initialice_ecuestre_permissions():
    ecuestre_role = Role.query.filter_by(name="Ecuestre").first()

    # Lista de permisos para el rol Ecuestre
    ecuestre_permissions = [
        "jya_index", "jya_show",
        "horse_index", "horse_new", "horse_show", "horse_update", "horse_destroy"
    ]

    for perm_name in ecuestre_permissions:
        permission = Permision.query.filter_by(name=perm_name).first()
        if permission:
            ecuestre_role.permissions.append(permission)

    db.session.commit()

def initialice_voluntariado_permissions():
    voluntariado_role = Role.query.filter_by(name="Voluntariado").first()

    # Lista de permisos para el rol Voluntariado
    voluntariado_permissions = [
        
    ]

    for perm_name in voluntariado_permissions:
        permission = Permision.query.filter_by(name=perm_name).first()
        if permission:
            voluntariado_role.permissions.append(permission)

    db.session.commit()    


def initialice_voluntariado_permissions():
    voluntariado_role = Role.query.filter_by(name="Voluntariado").first()

    # Lista de permisos para el rol Voluntariado
    voluntariado_permissions = [
        
    ]

    for perm_name in voluntariado_permissions:
        permission = Permision.query.filter_by(name=perm_name).first()
        if permission:
            voluntariado_role.permissions.append(permission)

    db.session.commit()    

def get_user_permissions(user_mail):
    if user_mail:
        user = User.query.filter_by(email=user_mail).first()
        user_permissions = {perm.name for perm in user.role.permissions}
    else:
        user_permissions = set()  # Usuario no autenticado, sin permisos
        return user_permissions, False
    return user_permissions, user.system_admin


def update_role(user, role):
    '''
        Permite dado un usuario y un rol cambiar el rol del usuario.
    '''
    user.role_id = role

    db.session.add(user)
    db.session.commit()

    return user

def get_all_roles():
    return Role.query.all()


def validate_all_form_fields(form):
    '''
        Valida que todos los campos del formulario de update_user estén correctos
    '''
    form_errors = form.errors
    for field in form:
        if field.errors:
            form_errors[field.name] = field.errors
    return form_errors