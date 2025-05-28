from housing_prices_dashboard.main import prepare_data

def map_dummy_variable(dummy_value: str) -> list[int]:
    categories = [
        'ocean_proximity_<1H OCEAN',
        'ocean_proximity_INLAND',
        'ocean_proximity_ISLAND',
        'ocean_proximity_NEAR BAY',
        'ocean_proximity_NEAR OCEAN'
    ]

    return [1 if dummy_value == cat.split('_')[2] else 0 for cat in categories]


if __name__ == "__main__":
    print(prepare_data(r'C:\Users\richard.macus\Desktop\housing_prices_app\housing_prices_dashboard\housing.csv')[0].columns)