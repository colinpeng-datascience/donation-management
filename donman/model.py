from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Type(db.Model):
    __tablename__ = 'type'
    type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.Text)

class Subtype(db.Model):
    __tablename__ = 'subtype'
    subtype_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_id = db.Column(db.Integer, db.ForeignKey('type.type_id'))
    subtype_name = db.Column(db.Text)
    __table_args__ = (db.UniqueConstraint('type_id', 'subtype_name'),)

class Donor(db.Model):
    __tablename__ = 'donor'
    donor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_email = db.Column(db.Text, unique=True)
    donor_name = db.Column(db.Text)

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_email = db.Column(db.Text, unique=True)
    staff_password_hashed = db.Column(db.Text)
    staff_name = db.Column(db.Text)
    staff_created_by_staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    staff_deleted_by_staff_id = db.Column(db.Boolean)
    __table_args__ = (
        db.ForeignKeyConstraint(['staff_created_by_staff_id'], ['staff.staff_id']),
        db.ForeignKeyConstraint(['staff_deleted_by_staff_id'], ['staff.staff_id']),
    )

class Donation(db.Model):
    __tablename__ = 'donation'
    donation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.donor_id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    donation_date = db.Column(db.Text)
    donation_quantity = db.Column(db.Integer)
    subtype_id = db.Column(db.Integer, db.ForeignKey('subtype.subtype_id'))
    __table_args__ = (
        db.ForeignKeyConstraint(['donor_id'], ['donor.donor_id']),
        db.ForeignKeyConstraint(['staff_id'], ['staff.staff_id']),
        db.ForeignKeyConstraint(['subtype_id'], ['subtype.subtype_id'])
    )

class Distribution(db.Model):
    __tablename__ = 'distribution'
    distribution_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    subtype_id = db.Column(db.Integer, db.ForeignKey('subtype.subtype_id'))
    distribution_date = db.Column(db.Text)
    distribution_amount = db.Column(db.Integer)
    __table_args__ = (
        db.ForeignKeyConstraint(['staff_id'], ['staff.staff_id']),
        db.ForeignKeyConstraint(['subtype_id'], ['subtype.subtype_id'])
    )