from geopy.geocoders import Nominatim


class ApiFunctions:

    def GetLatLon(self, address):
        geolocator = Nominatim(user_agent='myGeolocator')
        location = geolocator.geocode(address)
        if location:
            latitude = location.latitude
            longitude = location.longitude
        else:
            raise AttributeError ('Endereço não é válido')
