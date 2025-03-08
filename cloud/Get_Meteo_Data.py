def get_meteo_data(latitude, longitude, start_date, end_date):
    # Define the NASA POWER API URL
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR,PS,RH2M,T2MDEW,T2M,WS10M,WD10M,ALLSKY_SFC_SW_DWN&community=RE&longitude={longitude}&latitude={latitude}&start={start_date}&end={end_date}&format=JSON"
    
    # Send a GET request to fetch the data
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None