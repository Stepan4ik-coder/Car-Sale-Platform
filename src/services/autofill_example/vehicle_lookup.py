from src.schemas.cars import CarAutofillResponse


def autofill_example(vin: str):
    example_data = CarAutofillResponse(
        vin=vin,
        engine_type="diesel",
        litres=2,
        horse_power=97,
        year=1996,
        color="white",
        country="Japan",
    )

    return example_data
