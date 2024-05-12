import numpy as np
import pandera as pa
from pandera.typing import Series


class AmedasSchema(pa.DataFrameModel):
    timestamp: Series[np.datetime64]
    rainfall: Series[float] = pa.Field(ge=0, nullable=True)
    temperature: Series[float] = pa.Field(ge=0, nullable=True)
    humidity: Series[float] = pa.Field(ge=0, nullable=True)
    wind_speed: Series[float] = pa.Field(ge=0, nullable=True)
    wind_direction: Series[float] = pa.Field(ge=0, le=360, nullable=True)
    wind_speed_max: Series[float] = pa.Field(ge=0, nullable=True)
    wind_direction_max: Series[float] = pa.Field(ge=0, le=360, nullable=True)
    daylight_hours: Series[float] = pa.Field(ge=0, nullable=True)
