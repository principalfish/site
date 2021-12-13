# SQLite DB Schema

Current example files are in old folder


## Maps

Current data is in geojson format
Idea to construct geojson on fly from database using script
Which allows multiple maps
Old format is map.json


### Current JSON structure

Maps 
GeoJSON

* _objects_ 
	* _map_ 
		- _type_: GeometryCollection :
		- _geometries_: entry per seat, indexed
			+ _index_ : index of seat
				* _type_: Polygon 
				* _properties_ 
					- _region_ : north east england etc
					- _info_id_ : seat id within context of map
					- _name_ : seat  name
				* _arcs_ : maps to arcs property
	* _transform_  : relates to whewre the map is centred
		- _translate_ : lat long
		- _scale_ : x / y zoom?
	* _arcs_ : x / y entry per arc, indexed
 


### Database structure for maps

**Table : maps**
_maps_id_ : primary key
_name_ : eg UK 650
_type_ : eg GeometryCollection
_object_type : eg Polygon
_translate_lat_ : latitude centre default
_translate_long_ : longtitude centre default
_scale_x_: x zoom default 
_scale_y_ : y zoom default
 
**Table : seats**
_seats_id_ : primary key
_name_ : eg - Aberavon
_maps_id_ : maps to maps/maps_id
_region_id_ : maps to regions/region_id
_seat_in_map_id_ : index within the specific map
_arcs_ : maps to arc/arcs_id(multiple)

**Table : regions**
_regions_id_ : primary key
_code_: eg northeastengland
_name_ : eg North East England
_maps_id_ : maps to maps/map_id (multiple?)

**Table : arcs**
_arcs_id_ : primary key
_x0_ : point 0 x coord 
_y0_ : point 0 y coord
_x1_ : point 1 x coord
_y1_ : point 1 y coord


## Election

Current data is in json format
Idea to construct json on fly from database using script
Which allows multiple elections
Old format is election.json

### Current JSON structure

Self constructed json file - of specific election
* _seat_name_ : eg Aberavon
	- _partyInfo_ : one entry for each party
		*_party_shortcode__ : eg Labour
			* _total_ : votes cast
			* _name_ : candidate name
	- _seatInfo_ : specifid seat data
		+ _current_ : party short code
		+ _majority_ : majority
		+ _region_ : region short code
		+ _seat_name_ : eg Aberavon
		+ _electorate_ : electorate



### Database structure for elections

**Table : elections**
_elections_id_ : primary key
_election_name_: eg UK General 2019
_election_date_ : eg 01/01/2021
_maps_id_ : maps to maps/map_id
_previous_election_: maps to elections/elections_id (maybe?)

_**Table : partys**
_partys_id_ : primary key
_shortcode_ : eg lab (unique?)
_name_ : eg Labour
_country_ : eg UK

**Table : electorates**
_elections_id_ : maps to elections/elections_id
_electorate_ : electorate of seat in given election


**Table : votes**
_votes_id_ : primary key
_seats_id: maps to seats/seats_id
_elections_id_ : maps to elections/elections_id
_partys_id_ : maps to partys/partys_id
_votes_ : vote total
_candidate_ : Name of candidate (default to partys/name)


## Polls

Current data is in csv
Use to generate weighted averages / models in sync with other data


### Current CSV structure

_code_ : code of poll
_company_ : shortcode of company
_day_
_month_
_year_
_region_ : polling region 
_total votes_ : can be percentage or raw number
_per party vote total_ : can be percentage or number

### Database structure for polls

**Table : pollsters**
_pollsters_id : primary key
_shortcode_ : eg yougov1
_name_ : eg Yougov
_regions_ : maps to polling_regions/polls_regions_id (multiple)
_weight_ : relative weight of pollster
_type_ : percent or real (standardize to always be percent from input?)

**Table : polls**
_polls_id_: primary key
_date_ 
_pollsters_id_ : maps to pollsters/pollsters_id

**Table : polling_regions**
_polling_regions_id_ : primary key
_name_ : eg North
_subregions_: map to regions/regions_id (multiple)

**Table: polling_data**
_polling_data_id_ : primary_key
_polls_id_ : maps to polls/polls_id
_polling_regions_id_ : maps to polling_regions/polling_regions_id
_party_id_ : maps to partys/partys_id
_total_ : votes for party (standardize to percentage?)




## Future
Postcode data?
