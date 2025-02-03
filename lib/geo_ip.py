import geocoder
from transliterate import translit

# todo:
#  check url with translit according to current location
WEB_CITY = 'Костромская область'
translit(WEB_CITY, 'ru', reversed=True)
g = geocoder.ip('me')
city = g.current_result.city  # eng version
print(g.latlng)

