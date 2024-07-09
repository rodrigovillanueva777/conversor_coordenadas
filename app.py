#Version corregida
from flask import Flask, render_template, request
import utm

app = Flask(__name__)

# UTM zones data (simplified example, add more countries as needed)
utm_zones = {
    'Paraguay': '21S',
    'Brazil': '22S',
    'Argentina': '21S',
    'Chile': '19S',
    'Uruguay': '21S',
    'Puerto Rico': '20N',
    # Add more countries and zones as needed
}

@app.route('/')
def index():
    return render_template('index.html', utm_zones=utm_zones.keys())

@app.route('/convert', methods=['POST'])
def convert():
    conversion_type = request.form['conversion_type']
    try:
        if conversion_type == 'utm_to_latlon':
            easting = float(request.form['easting'])
            northing = float(request.form['northing'])
            zone_number = int(request.form['zone_number'])
            zone_letter = request.form['zone_letter'].upper()
            lat, lon = utm.to_latlon(easting, northing, zone_number, zone_letter)
            result = f"Lat: {lat:.6f}°, Lon: {lon:.6f}°"
            dms_lat = decimal_to_dms(lat, is_lat=True)
            dms_lon = decimal_to_dms(lon, is_lat=False)
            google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
            return render_template('index.html', result=result, dms_lat=dms_lat, dms_lon=dms_lon, google_maps_link=google_maps_link, utm_zones=utm_zones.keys())
        elif conversion_type == 'latlon_to_utm':
            lat = float(request.form['lat'])
            lon = float(request.form['lon'])
            utm_coords = utm.from_latlon(lat, lon)
            result = f"X: {utm_coords[0]}, Y: {utm_coords[1]}, Zona: {utm_coords[2]}{utm_coords[3]}"
            return render_template('index.html', result=result, utm_zones=utm_zones.keys())
    except Exception as e:
        print(e)
        error_message = "Datos incorrectos, vuelva a verificar."
        return render_template('index.html', error_message=error_message, utm_zones=utm_zones.keys())

@app.route('/search_zone', methods=['POST'])
def search_zone():
    country = request.form['country']
    zone = utm_zones.get(country, 'No disponible')
    return render_template('index.html', search_result=f"Zona UTM para {country}: {zone}", utm_zones=utm_zones.keys(), country=country, zone=zone)

def decimal_to_dms(decimal, is_lat):
    degrees = int(decimal)
    minutes_float = abs((decimal - degrees) * 60)
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60
    if is_lat:
        direction = 'S' if decimal < 0 else 'N'
    else:
        direction = 'O' if decimal < 0 else 'E'
    return f"{abs(degrees)}°{minutes}'{seconds:.2f}\"{direction}"

if __name__ == '__main__':
    app.run(debug=True)
