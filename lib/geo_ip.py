import geocoder
from transliterate import translit

WEB_CITY = 'Костромская область'
translit(WEB_CITY, 'ru', reversed=True)
g = geocoder.ip('me')
city = g.current_result.city  # eng version
print(g.latlng)

