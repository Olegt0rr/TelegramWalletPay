from pydantic import BaseModel, ConfigDict

from telegram_wallet_pay.tools import from_snake_to_camel


class DefaultModel(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        alias_generator=from_snake_to_camel,
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )
