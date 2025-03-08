current_date = datetime.utcnow()
start_date = current_date
end_date = current_date

data = get_meteo_data(latitude, longitude, start_date, end_date)

if data:
    try:
        dates = list(data['properties']['parameter']['PRECTOTCORR'].keys())
        
        required_parameters = ['PRECTOTCORR', 'PS', 'RH2M', 'T2MDEW', 'T2M', 'WS10M', 'WD10M', 'ALLSKY_SFC_SW_DWN']
        default_values = {
            'PRECTOTCORR': 0.0,
            'PS': 1013.25,
            'RH2M': 50.0,
            'T2MDEW': 10.0,
            'T2M': 20.0,
            'WS10M': 3.0,
            'WD10M': 180.0,
            'ALLSKY_SFC_SW_DWN': 200.0
        }

        parameters_data = {param: data['properties']['parameter'].get(param, {}) for param in required_parameters}
        
        df = pd.DataFrame({
            date: {
                param: parameters_data[param].get(date, default_values[param]) if parameters_data[param].get(date, -999.00) != -999.00 else default_values[param]
                for param in required_parameters
            }
            for date in dates
        }).T

        df.index.name = 'Date'

    except KeyError as e:
        print(f"Error extracting data: {e}")
else:
    print("No data returned from the API.")

# Get the first row of the DataFrame
first_row = df.iloc[0]

# Extract the date and parameters
date_str = first_row.name
date = pd.to_datetime(date_str, format='%Y%m%d')
year = date.year
month = date.month
day = date.day
day_of_week = date.day_name()  
is_weekend = day_of_week in ['Saturday', 'Sunday']
week_of_year = date.isocalendar()[1]  
quarter = date.quarter

# Extract parameters
PRECTOTCORR = first_row['PRECTOTCORR']
PS = first_row['PS']
RH2M = first_row['RH2M']
T2MDEW = first_row['T2MDEW']
T2M = first_row['T2M']
WS10M = first_row['WS10M']
WD10M = first_row['WD10M']
ALLSKY_SFC_SW_DWN = first_row['ALLSKY_SFC_SW_DWN']

# Encode the day_of_week
label_encoder = LabelEncoder()
day_of_week_encoded = label_encoder.fit_transform([day_of_week])[0]
# Print the extracted values
print(f"Date: {date_str}")
print(f"Year: {year}")
print(f"Month: {month}")
print(f"Day: {day}")
print(f"Day of the Week: {day_of_week}")
print(f"Is Weekend: {is_weekend}")
print(f"Week of the Year: {week_of_year}")
print(f"Quarter: {quarter}")
print(f"PRECTOTCORR: {PRECTOTCORR}")
print(f"PS: {PS}")
print(f"RH2M: {RH2M}")
print(f"T2MDEW: {T2MDEW}")
print(f"T2M: {T2M}")
print(f"WS10M: {WS10M}")
print(f"WD10M: {WD10M}")
print(f"ALLSKY_SFC_SW_DWN: {ALLSKY_SFC_SW_DWN}")
# Prepare new data for prediction
model = joblib.load('rain_model.pkl')
new_data = [[
    PRECTOTCORR,
    PS,
    RH2M,
    T2MDEW,
    T2M,
    WS10M,
    WD10M,
    ALLSKY_SFC_SW_DWN,
    year,
    month,
    day,
    day_of_week_encoded,  # Use the encoded value
    is_weekend,
    week_of_year,
    quarter
]]

new_data_df = pd.DataFrame(new_data, columns=[
    'PRECTOTCORR',
    'PS',
    'RH2M',
    'T2MDEW',
    'T2M',
    'WS10M',
    'WD10M',
    'ALLSKY_SFC_SW_DWN',
    'year',
    'month',
    'day',
    'day_of_week',  # Note: This is now encoded
    'is_weekend',
    'week_of_year',
    'quarter'
])

# Make a prediction
predicted_rain = model.predict(new_data_df)
if (predicted_rain[0]==0):
    print(" predicted_rain:","NO" )
else:
  print("predicted_rain:","YES"  )
