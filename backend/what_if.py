from typing import Optional
from pydantic import BaseModel


class WhatIfRequest(BaseModel):
    current_yield: float
    fertilizer_change_percent: float = 0
    rainfall_change_percent: float = 0
    irrigation_change_percent: float = 0


class WhatIfResponse(BaseModel):
    current_yield: float
    estimated_yield: float
    yield_change: float
    yield_change_percent: float
    message: str


def calculate_what_if(data: WhatIfRequest) -> WhatIfResponse:
    current_yield = max(0, data.current_yield)

    fertilizer_effect = data.fertilizer_change_percent * 0.002
    rainfall_effect = data.rainfall_change_percent * 0.001
    irrigation_effect = data.irrigation_change_percent * 0.0015

    total_effect = (
        fertilizer_effect
        + rainfall_effect
        + irrigation_effect
    )

    total_effect = max(-0.30, min(0.30, total_effect))

    estimated_yield = current_yield * (1 + total_effect)

    yield_change = estimated_yield - current_yield

    if current_yield > 0:
        yield_change_percent = (
            yield_change / current_yield
        ) * 100
    else:
        yield_change_percent = 0

    if yield_change_percent > 5:
        message = "Expected yield improvement."
    elif yield_change_percent < -5:
        message = "Expected yield reduction."
    else:
        message = "Expected yield remains relatively stable."

    return WhatIfResponse(
        current_yield=round(current_yield, 2),
        estimated_yield=round(estimated_yield, 2),
        yield_change=round(yield_change, 2),
        yield_change_percent=round(yield_change_percent, 2),
        message=message,
    )