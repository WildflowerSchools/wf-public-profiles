# Import all the models, so that Base has them before being
# imported by Alembic
from .base_class import Base  # noqa
from wf_public_profiles.models import public_profile

# from app.models.item import Item  # noqa
# from app.models.user import User  # noqa
