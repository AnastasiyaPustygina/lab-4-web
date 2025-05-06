import sys
import os
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import logging
# Set the path for the app context
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize the Flask app

from app import create_app
app = create_app()

# Get the Alembic configuration and logger
config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

def get_engine():
    """Retrieve the database engine."""
    # Use app context for current_app to be available
    with app.app_context():
        try:
            return app.extensions['migrate'].db.get_engine()
        except (TypeError, AttributeError):
            return app.extensions['migrate'].db.engine

def get_engine_url():
    """Return the database URL."""
    with app.app_context():
        try:
            return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
        except AttributeError:
            return str(get_engine().url).replace('%', '%%')

# Set the target metadata
def get_metadata():
    """Get metadata for auto-generation."""
    with app.app_context():
        target_db = app.extensions['migrate'].db
        if hasattr(target_db, 'metadatas'):
            return target_db.metadatas[None]
        return target_db.metadata

config.set_main_option('sqlalchemy.url', get_engine_url())

# Running migrations offline
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=get_metadata(), literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

# Running migrations online
def run_migrations_online():
    """Run migrations in 'online' mode."""
    with app.app_context():  # Ensure app context is available here
        connectable = get_engine()

        with connectable.connect() as connection:
            context.configure(connection=connection, target_metadata=get_metadata())

            with context.begin_transaction():
                context.run_migrations()

# Run migrations based on the mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
