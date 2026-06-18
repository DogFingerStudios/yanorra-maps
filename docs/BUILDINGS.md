# Buildings

Buildings should go in one of two layers
- `buildings_major.geojson` for important landmarks, castles, palaces, etc.
- `buildings_minor.geojson` for typical houses, shops, inns, etc.

Each building feature can have fields like:

```text
id
  Type: Text
  Purpose: Stable unique feature ID
  Examples: bldg_gunsey_police_station, bldg_port_sable_customs_house

name
  Type: Text
  Purpose: Display name
  Examples: Gunsey Police Station, Old Harbor Customs House, North Watchtower

settlement_id
  Type: Text
  Purpose: Settlement this building belongs to
  Examples: stl_gunsey, stl_port_sable, stl_sunshine_beach

country_id
  Type: Text
  Purpose: Nation this building belongs to
  Examples: nation_barrel, nation_duvessa, nation_velu

district_id
  Type: Text
  Purpose: Optional district/neighborhood/ward
  Examples: dist_port_sable_old_harbor, dist_gunsey_market_square

building_type
  Type: Text
  Purpose: Broad category
  Possible values:
    civic
    government
    religious
    commercial
    industrial
    residential
    military
    fortification
    transport
    harbor
    educational
    medical
    cultural
    utility
    agricultural
    landmark
    ruin
    other
    unknown

building_subtype
  Type: Text
  Purpose: Specific kind of building
  Possible values:
    town_hall
    courthouse
    police_station
    jail
    guardhouse
    customs_house
    governor_house
    temple
    shrine
    cathedral
    chapel
    market_hall
    shop
    inn
    tavern
    warehouse
    factory
    mill
    workshop
    lighthouse
    rail_station
    ferry_terminal
    dock_office
    barracks
    fort
    watchtower
    gatehouse
    school
    library
    hospital
    clinic
    theater
    museum
    manor
    granary
    waterworks
    power_station
    farmstead
    ruin
    monument
    other
    unknown

status
  Type: Text
  Purpose: Current condition/use
  Possible values:
    active
    abandoned
    ruined
    damaged
    under_construction
    planned
    closed
    repurposed
    seasonal
    restricted
    unknown

access
  Type: Text
  Purpose: Who can enter/use it
  Possible values:
    public
    restricted
    private
    military
    government
    staff_only
    ceremonial
    closed
    unknown

importance
  Type: Text
  Purpose: How prominent it is on the map/lore
  Possible values:
    local
    district
    settlement
    regional
    national
    historic
    iconic

wiki_id
  Type: Text
  Purpose: Optional wiki entry ID
  Examples: bldg_gunsey_police_station, wiki_old_harbor_customs_house

label_rank
  Type: Integer
  Purpose: Label priority; lower or higher is your choice, just be consistent
  Examples:
    1 = most important
    2 = important
    3 = local landmark
    4 = minor named building

zoom_min
  Type: Integer
  Purpose: Minimum website zoom level where this building appears
  Examples:
    12
    13
    14
    15
    16

notes
  Type: Text
  Purpose: Freeform notes
  Examples: Small-town police station near the main road.
```