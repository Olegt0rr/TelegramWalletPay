from pydantic import BaseModel, ConfigDict, RootModel

from telegram_wallet_pay.tools import from_snake_to_camel

_model_config = ConfigDict(
    use_enum_values=True,
    alias_generator=from_snake_to_camel,
    populate_by_name=True,
    validate_assignment=True,
    arbitrary_types_allowed=True,
)


class DefaultModel(BaseModel):
    model_config = _model_config


class DefaultRootModel(RootModel):
    model_config = _model_config
