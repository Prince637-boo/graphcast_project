import cdsapi

# Initialisation du client Copernicus
c = cdsapi.Client()

# Définir la zone géographique : Afrique de l’Ouest
# Format: [nord, ouest, sud, est]
region = [20, -20, 0, 20]

# Variables de niveau supérieur nécessaires à GraphCast
upper_vars = [
    'geopotential',
    'temperature',
    'u_component_of_wind',
    'v_component_of_wind',
    'specific_humidity'
]

# Variables de surface
surface_vars = [
    '2m_temperature',
    '10m_u_component_of_wind',
    '10m_v_component_of_wind',
    'mean_sea_level_pressure'
]

# Dates : exemple du 1er janvier 2023, T0 et T-6h
dates = ['2023-01-01T00:00', '2022-12-31T18:00']

for date in dates:
    year, month, day_time = date.split('-')
    day, hour = day_time.split('T')
    print(f"Téléchargement des données ERA5 pour {date}...")

    c.retrieve(
        'reanalysis-era5-complete',
        {
            'class': 'ea',
            'date': f'{year}-{month}-{day}',
            'expver': '1',
            'levtype': 'pl',
            'levelist': [1000, 850, 500, 300, 200, 100],  # Niveaux de pression choisis
            'param': [
                '129.128',  # géopotentiel
                '130.128',  # température
                '131.128',  # vent U
                '132.128',  # vent V
                '133.128',  # humidité spécifique
            ],
            'stream': 'oper',
            'time': hour + ':00',
            'area': region,
            'format': 'netcdf',
        },
        f'era5_upper_{hour.replace(":","")}.nc'
    )

    # Variables de surface
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'variable': surface_vars,
            'year': year,
            'month': month,
            'day': day,
            'time': hour + ':00',
            'area': region,
            'format': 'netcdf',
        },
        f'era5_surface_{hour.replace(":","")}.nc'
    )

print("✅ Téléchargement terminé !")
