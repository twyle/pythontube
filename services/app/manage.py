"""This module starts the application."""
from api import create_app, db
from flask.cli import FlaskGroup

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("create_db")
def create_db():
    """Create the database and all the tables."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    
    
@cli.command("seed_db")
def seed_db():
    """Create the database and all the tables."""
    pass


if __name__ == "__main__":
    cli()
