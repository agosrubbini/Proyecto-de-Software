from src.core.database import db


role_permission = db.Table(
    "role_permission",
    db.Column(db.Integer, db.ForeignKey("roles.id")),
    db.Column(db.Integer, db.ForeignKey("permissions.id"))
)
    

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    permissions = db.relationship("Permissions", secondary=role_permission, backref="role")

    def __repr__(self):
        return f'<Role #{self.name}>'


class Permisions(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Role #{self.name}>'    
