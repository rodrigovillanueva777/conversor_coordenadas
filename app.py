from flask import Flask, render_template, request
from pyproj import Proj, transform

app = Flask(__name__)

def utm_to_latlon(easting, northing, zone_number, zone_letter):
    utm_proj = Proj(proj='utm', zone=zone_number, datum='WGS84', south=(zone_letter.lower() >= 'n'))
    latlon_proj = Proj(proj='latlong', datum='WGS84')
    lon, lat = transform(utm_proj, latlon_proj, easting, northing)
    return lat, lon

def latlon_to_utm(lat, lon):
    utm_proj = Proj(proj='utm', zone=int((lon + 180) / 6) + 1, datum='WGS84', south=(lat < 0))
    easting, northing = transform(Proj(proj='latlong', datum='WGS84'), utm_proj, lon, lat)
    zone_number = int((lon + 180) / 6) + 1
    zone_letter = 'N' if lat >= 0 else 'S'
    return easting, northing, zone_number, zone_letter

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    conversion_type = request.form['conversion_type']
    
    if conversion_type == 'utm_to_latlon':
        easting = float(request.form['easting'])
        northing = float(request.form['northing'])
        zone_number = int(request.form['zone_number'])
        zone_letter = request.form['zone_letter']
        lat, lon = utm_to_latlon(easting, northing, zone_number, zone_letter)
        return render_template('index.html', result=f"Lat: {lat}, Lon: {lon}")

    elif conversion_type == 'latlon_to_utm':
        lat = float(request.form['lat'])
        lon = float(request.form['lon'])
        easting, northing, zone_number, zone_letter = latlon_to_utm(lat, lon)
        return render_template('index.html', result=f"Easting: {easting}, Northing: {northing}, Zone: {zone_number}{zone_letter}")

if __name__ == '__main__':
    app.run(debug=True)
