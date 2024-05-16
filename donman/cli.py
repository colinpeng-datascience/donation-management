from donman.model import Type, Staff, Subtype
from werkzeug.security import generate_password_hash
from donman.controller import db
import click
from donman import app as current_app

@current_app.cli.command("init-db")
def init_db_command():
    """Initialize the database with initial data."""
    try:
        with current_app.app_context():
            # Check if initial data already exists
            if not Type.query.filter_by(type_name="other").first():
                # Create initial data if it doesn't exist
                type_other = Type(type_name="other")
                db.session.add(type_other)
                db.session.commit()
                

                new_subtype = Subtype(type_id=type_other.type_id, subtype_name="other")
                db.session.add(new_subtype)
                
                db.session.commit()

                click.echo("Added initial data 'other'.")
            else:
                click.echo("initial data 'other' already exists. Skipping.")

            if not Staff.query.filter_by(staff_email=current_app.config["ADMIN_EMAIL"]).first():
                # Create admin staff if it doesn't exist
                hashed_password = generate_password_hash(current_app.config["ADMIN_PASSWORD"])
                init_staff = Staff(
                    staff_email=current_app.config["ADMIN_EMAIL"],
                    staff_password_hashed=hashed_password,
                    staff_name=current_app.config["ADMIN_NAME"]
                )
                db.session.add(init_staff)
                db.session.commit()
                click.echo("Added admin staff.")
            else:
                click.echo("Admin staff already exists. Skipping.")
    except Exception as e:
        click.echo(f"An error occurred during database initialization: {str(e)}")
