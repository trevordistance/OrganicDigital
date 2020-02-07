################################################################################
import warnings
# THIS SUPPRESSION ISN'T WORKING - WHY NOT?
warnings.filterwarnings('ignore', message='InsecureRequestWarning')
################################################################################
import math
import googlemaps
from googleplaces import GooglePlaces, types, lang
import folium
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
################################################################################
# prep map background using Morecambe as a centre point
m = folium.Map(location=[54.093409, -2.89479],
    tiles='stamenwatercolor',
    zoom_start=6,
    crs='EPSG3857',
    )
###############################################################################
# define the list of cities to be processed
cities=('birkenhead','bootle','bradford','bury','cannock','chelmsford','chesterfield','coventry','dundee','durham','east-kilbride','glasgow-g1','hartlepool','liverpool','livingston','maidstone','middlesbrough','newcastle-upon-tyne','nuneaton','oldham','preston','sheffield','st-helens','walsall','widnes')
# test cities
#cities=('birkenhead','bradford')
# for step through with a single city
city='bury'
# create city_data to hold collected data during processing
city_data = []
###############################################################################
# loop through cities and gather relevant information
for city in cities:
    working_city = city.title()
    store_name = 'TJ Hughes ' + working_city
# set up a connection to GoogleMaps
    gmaps = googlemaps.Client(key='API_KEY')
# get place_id for the store location
    geocode_result = gmaps.geocode(store_name)
# the result is returned as a list of length one, with a lot of info crammed in
# convert the list to be a string in order to parse it then split
    geocode_result=(str(geocode_result))
    geocode_result=geocode_result.split(",")
# split returned a list, so convert to string, split, create place_id
    geocode_result=str(geocode_result)
    geocode_result=geocode_result.split("'place_id': '",1)[1]
    place_id=geocode_result[:geocode_result.index("'")]
# connect to GooglePlaces
    google_places = GooglePlaces('API_KEY')
# query GooglePlaces with place_id to get place information
    places_result = google_places.get_place(place_id=place_id)
# convert place information from type googleplaces.Place to a string
    places_result=str(places_result)
# split the places_result to get latitude
    places_result=places_result.split("lat=",1)[1]
    lat=places_result[:places_result.index(",")]
# split places_result_strip to get longitude
    lng=places_result.split("lng=",1)[1]
    lng=lng[:lng.index(">")]
# define the query for googleapis
    api_query = 'https://maps.googleapis.com/maps/api/place/details/xml?place_id='+place_id+'&fields=name,rating,user_ratings_total&key=API_KEY'
# store the query result as page
    page = requests.get(api_query, verify=False)
# parse the query result
    soup_r = BeautifulSoup(page.text, 'lxml')
    rating = soup_r.rating
# parse and process for user_ratings_total
    user_ratings_total = soup_r.user_ratings_total
    user_ratings_total=str(user_ratings_total)
    user_ratings_total=user_ratings_total.split("<user_ratings_total>",1)[1]
    user_ratings_total=user_ratings_total[:user_ratings_total.index("<")]
# parse and process for rating
    rating=str(rating)
    rating=rating.split("<rating>",1)[1]
    rating=rating[:rating.index("<")]
# prepare working_city_data
    working_city_data=[working_city,lat,lng,rating,user_ratings_total]
# prepare a summary to appear as a popup string, based on working_city_data
    popup_string=working_city_data[0]+', Rating = '+working_city_data[3]+' from '+working_city_data[4]+' reviews'
# add popup_string to working_city_data
# should this be done as an append etc?
    working_city_data=[working_city,lat,lng,rating,user_ratings_total,popup_string]
# use city_data to hold the data for all working_city_data during processing
    city_data.append(working_city_data)
# create a dataframe and insert the city_data of working_city_data as a new row
    df=pd.DataFrame(city_data,columns=['Store', 'Lat', 'Lng', 'Rating', 'Quantity', 'Popup String'])
# add a point on the map using the co-ordinates for the city
    folium.Circle(location=[working_city_data[1], working_city_data[2]],
              popup=popup_string,
              radius=math.sqrt(float(working_city_data[4]))*1000,
              color='black',
              fill=True,
              fill_color='yellow').add_to(m)
###############################################################################
# save the map
m.save('OrganicDigital/TJHughes.html')
# record the date as a variable
today = datetime.date.today()
# add a column to df to hold the date
df['Date'] = today
# write the dataframe to a file
export_csv = df.to_csv (r'OrganicDigital/TJHughes.csv', index = None, header=True)
###############################################################################
# clear dataframe and city_data to avoid multiple runs being merged
###############################################################################
df.drop(df.index, inplace=True)
city_data.clear()
