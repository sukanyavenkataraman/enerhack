import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pvlib
from pvlib.forecast import GFS

latitude, longitude, tzo = 44.801817, -69.890908, 'US/Central'

def get_irradiance(lat=latitude, lon=longitude, tz=tzo, intervals_of_3=1, time=datetime.datetime.now()+datetime.timedelta(hours=-5)):
    start = pd.Timestamp(time, tz=tz)

    end = start + pd.Timedelta(hours=3 * intervals_of_3)
    irrad_vars = ['ghi', 'dni', 'dhi']

    print (start, end)
    model = GFS()
    raw_data = model.get_data(lat, lon, start, end)

    # print(raw_data.head())

    data = raw_data
    data = model.rename(data)
    data['temp_air'] = model.kelvin_to_celsius(data['temp_air'])
    data['wind_speed'] = model.uv_to_speed(data)
    irrad_data = model.cloud_cover_to_irradiance(data['total_clouds'])
    data = data.join(irrad_data, how='outer')
    data = data[model.output_variables]

    data = model.rename(raw_data)
    irrads = model.cloud_cover_to_irradiance(data['total_clouds'], how='clearsky_scaling')

    # change this to list when taking more than one values
    return (irrads.ghi.values.tolist()), (data['total_clouds'].values / 100)


if __name__ == "__main__":
    get_irradiance(latitude, longitude, tzo)

# offset = 0.35
#
# solpos = location.get_solarposition(cloud_cover.index)
# cs = location.get_clearsky(cloud_cover.index, model='ineichen')
# # offset and cloud cover in decimal units here
# # larson et. al. use offset = 0.35
# ghi = (offset + (1 - offset) * (1 - cloud_cover)) * ghi_clear
# dni = disc(ghi, solpos['zenith'], cloud_cover.index)['dni']
# dhi = ghi - dni * np.cos(np.radians(solpos['zenith']))
