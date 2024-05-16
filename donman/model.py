from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Type(db.Model):
    __tablename__ = 'type'
    type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.Text, unique=True, nullable=False)
    def serialize(self):
        """Return type data in serialized format"""
        return {
            'id': self.type_id,
            'name': self.type_name,
        }

class Subtype(db.Model):
    __tablename__ = 'subtype'
    subtype_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_id = db.Column(db.Integer, db.ForeignKey('type.type_id'))
    subtype_name = db.Column(db.Text, nullable=False)
    __table_args__ = (db.UniqueConstraint('type_id'),)
    def serialize(self):
        """Return subtype data in serialized format"""
        return {
            'id': self.subtype_id,
            'name': self.subtype_name,
        }
class Donor(db.Model):
    __tablename__ = 'donor'
    donor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_email = db.Column(db.Text, unique=True, nullable=False)
    donor_name = db.Column(db.Text, nullable=False)
    def serialize(self):
        """Return donor data in serialized format"""
        return {
            'id': self.donor_id,
            'email': self.donor_email,
            'name': self.donor_name,
        }
class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_email = db.Column(db.Text, unique=True, nullable=False)
    staff_password_hashed = db.Column(db.Text, nullable=False)
    staff_name = db.Column(db.Text, nullable=False)
    staff_created_by_staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=True)
    staff_deleted_by_staff_id = db.Column(db.Boolean)
    __table_args__ = (
        db.ForeignKeyConstraint(['staff_created_by_staff_id'], ['staff.staff_id']),
        db.ForeignKeyConstraint(['staff_deleted_by_staff_id'], ['staff.staff_id']),
    )
    def serialize(self):
        """Return staff data in serialized format"""
        return {
            'id': self.staff_id,
            'name': self.staff_name,
            'email': self.staff_email
        }

class Donation(db.Model):
    __tablename__ = 'donation'
    donation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.donor_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=False)
    donation_date = db.Column(db.DateTime, default=datetime.now)
    donation_quantity = db.Column(db.Integer, nullable=False)
    subtype_id = db.Column(db.Integer, db.ForeignKey('subtype.subtype_id'), nullable=False)
    __table_args__ = (
        db.ForeignKeyConstraint(['donor_id'], ['donor.donor_id']),
        db.ForeignKeyConstraint(['staff_id'], ['staff.staff_id']),
        db.ForeignKeyConstraint(['subtype_id'], ['subtype.subtype_id'])
    )

class Distribution(db.Model):
    __tablename__ = 'distribution'
    distribution_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=False)
    subtype_id = db.Column(db.Integer, db.ForeignKey('subtype.subtype_id'), nullable=False)
    distribution_date = db.Column(db.DateTime, default=datetime.now)
    distribution_amount = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.ForeignKeyConstraint(['staff_id'], ['staff.staff_id']),
        db.ForeignKeyConstraint(['subtype_id'], ['subtype.subtype_id'])
    )