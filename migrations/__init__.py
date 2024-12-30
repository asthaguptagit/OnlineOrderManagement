from flask import current_app
from alembic import context
from sqlalchemy import engine_from_config, pool

def get_engine_url():
    return current_app.config.get('DATABASE_URL')

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_engine_url()
    context.configure(url=url, target_metadata=None, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        current_app.config['DATABASE_URL'],
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=None
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
