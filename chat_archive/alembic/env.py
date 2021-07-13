# Easy to use offline chat archive.
#
# Author: Peter Odding <peter@peterodding.com>
# Last Change: June 30, 2018
# URL: https://github.com/xolox/python-chat-archive

"""
Automated database migrations for the `chat-archive` program.

Alembic_ is used to implement automated database migrations. This Python script
was originally generated by the ``alembic init`` command, however by default
Alembic expects the database connection string to be hard coded inside a
configuration file. That really won't work for our use case so this Python
script has been modified to ask :mod:`chat_archive` for the connection
string (`more details <http://stackoverflow.com/a/22179047/788200>`_).

.. _Alembic: http://alembic.zzzcomputing.com/
"""

# External dependencies.
from alembic import context
from sqlalchemy import engine_from_config, pool

# Modules included in our package.
from chat_archive import ChatArchive
from chat_archive.models import Base


def run_migrations():
    """Configure Alembic and execute any pending migrations."""
    # Get the database connection string for Alembic from an instance of
    # compact-backups iff the connection string isn't already available.
    if not context.config.get_main_option("sqlalchemy.url"):
        program = ChatArchive(auto_create_schema=False, auto_upgrade_schema=False)
        context.config.set_main_option("sqlalchemy.url", program.database_url)
    # Execute any pending migrations in the requested mode.
    (run_migrations_offline if context.is_offline_mode() else run_migrations_online)(
        # Enable a workaround that provides `proper' database migrations for
        # SQLite databases (which lacks complete `ALTER TABLE' semantics).
        render_as_batch=True,
        # Enable `alembic revision --autogenerate' to introspect
        # the current database schema during local development.
        target_metadata=Base.metadata,
    )


def run_migrations_offline(**options):
    """Run migrations in 'offline' mode."""
    context.configure(
        # Enable 'offline' mode.
        literal_binds=True,
        url=context.config.get_main_option("sqlalchemy.url"),
        # Pass on the common options.
        **options
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(**options):
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            # Enable 'online' mode.
            connection=connection,
            # Pass on the common options.
            **options
        )
        with context.begin_transaction():
            context.run_migrations()


# Execute any pending migrations when this script is run.
run_migrations()
