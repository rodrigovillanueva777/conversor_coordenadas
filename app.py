from flask import Flask, request, render_template
import utm
import re

app = Flask(__name__)

def dms_to_decimal(dms_str):
    dms_str = re.sub(r'[^0-9NSEW.]+', ' ', dms_str).strip()
    parts = dms_str.split(' ')
    
    if len(parts) != 4:
        raise ValueError('DMS input should be in the format: 51°28\'40.12"N 0°0\'5.31"W')
    
    lat_d = float(parts[0])
    lat_m = float(parts[1])
    lat_s = float(parts[2])
    lat_dir = parts[3]

    lon_d = float(parts[4])
    lon_m = float(parts[5])
    lon_s = float(parts[6])
    lon_dir = parts[7]

    lat = lat_d + (lat_m / 60.0) + (lat_s / 3600.0)
    if lat_dir == 'S':
        lat = -lat

    lon = lon_d + (lon_m / 60.0) + (lon_s / 3600.0)
    if lon_dir == 'W':
        lon = -lon

    return lat, lon

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    result = ''
    error_message = ''
    google_maps_link = ''
    lat = None
    lon = None
    dms_lat = request.form.get('dms_lat', '')
    dms_lon = request.form.get('dms_lon', '')

    if request.form.get('conversion_type') == 'utm_to_latlon':
        try:
            easting = float(request.form.get('easting'))
            northing = float(request.form.get('northing'))
            zone_number = int(request.form.get('zone_number'))
            zone_letter = request.form.get('zone_letter')

            lat, lon = utm.to_latlon(easting, northing, zone_number, zone_letter)
            result = f'Lat: {lat}, Lon: {lon}'
            google_maps_link = f'https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}'
        except Exception as e:
            error_message = str(e)

    elif request.form.get('conversion_type') == 'latlon_to_utm':
        try:
            if dms_lat and dms_lon:
                lat, lon = dms_to_decimal(f"{dms_lat} {dms_lon}")
            else:
                lat = float(request.form.get('lat'))
                lon = float(request.form.get('lon'))
            
            u = utm.from_latlon(lat, lon)
            result = f'X: {u[0]}, Y: {u[1]}, Zone Number: {u[2]}, Zone Letter: {u[3]}'
            google_maps_link = f'https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}'
        except Exception as e:
            error_message = str(e)

    return render_template('index.html', result=result, google_maps_link=google_maps_link, lat=lat, lon=lon, error_message=error_message)

@app.route('/search_zone', methods=['POST'])
def search_zone():
    country = request.form.get('country')
    # Aquí debes implementar la lógica para buscar la zona UTM basada en el país
    # Por simplicidad, en este ejemplo, no se ha implementado esa lógica
    return render_template('index.html', result=f'Zona UTM para {country}')

if __name__ == '__main__':
    app.run(debug=True)
