from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Entity(BaseModel):
    """
    Base entity model with common fields.

    Attributes:
        id (UUID): Unique identifier for the entity.
        created_at (datetime): Timestamp indicating when the entity was created.
        updated_at (datetime): Timestamp indicating when the entity was last updated.
        is_active (bool): Flag indicating whether the entity is active.

    Raises:
        ValueError: If any of the fields do not conform to their expected types.

    Example:
        entity = Entity(
            id=UUID('123e4567-e89b-12d3-a456-426655440000'),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True
        )
    """

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    def __eq__(self, other):
        """
        Test for equality between two entities.

        Args:
            other (Entity): The other entity to compare.

        Returns:
            bool: True if the entities are equal, False otherwise.
        """

        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id
