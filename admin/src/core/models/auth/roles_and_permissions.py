from src.core.database import db


role_permission = db.Table(
    "role_permission",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"))
)
    

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum("Técnica", "Ecuestre", "Voluntariado", "Administración", "Sin rol", name="name"), nullable=False)
    permissions = db.relationship("Permission", secondary=role_permission, backref="role")

    def __repr__(self):
        return f'<Role #{self.name}>'


class Permision(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Role #{self.name}>'    
