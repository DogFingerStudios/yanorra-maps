## Labels

The label layer layout is as follows:

```
labels/
  political_labels.geojson  - LineString; political entities, such as countries, states, and cities
  landform_labels.geojson   - LineString; natural landforms, such as mountains, valleys, and deserts
  water_labels.geojson      - LineString; bodies of water, such as rivers, lakes, and oceans
  settlement_labels.geojson - Point     ; human settlements, such as towns and cities
  route_labels.geojson      - LineString; transportation routes, such as roads and railways
  lore_labels.geojson       - LineString; fictional or historical locations
```

Each of these can contain the same fields:

```
id              string   Stable ID for this label feature
target_id       string   ID of the thing being labeled
label_text      string   Text shown on map
label_type      string   Specific kind of label
rank            integer  Importance; 1 = most important
min_zoom        number   First zoom level where label appears
max_zoom        number   Last zoom level where label appears
font_size       number   Suggested base font size
font_style      string   normal | italic
font_weight     string   300 | 400 | 500 | 600 | 700
text_transform  string   none | uppercase | small_caps
letter_spacing  number   Space between letters
placement       string   center | offset | along_line | approximate
start_offset    string   example: "40%", "12px", default: "50%"
text_anchor     string   start | middle | end
repeat          boolean  Whether to repeat along a line
visibility      string   default | hidden | lore | admin | debug
certainty       string   confirmed | approximate | disputed | speculative
notes           string   Optional internal notes
```

## Seaways

For `seaways`, I’d treat this as a **route/path layer**, not a label layer.

So the geometry is probably:

```text
seaways.geojson - LineString
```

This layer represents actual navigable or historically attempted sea routes.

---

# Recommended fields for `seaways`

```text
id              string
name            string
seaway_type     string
status          string
rank            integer
hazard_level    string
certainty       string
seasonality     string
traffic_level   string
start_id        string
end_id          string
notes           string
```

Optional later:

```text
wiki_id         string
source_type     string
last_confirmed  string
```

---

# Field meanings

## `id`

Stable canonical ID.

Examples:

```text
sea_sable_thaurin
sea_brooding_crossing
sea_lost_eastvoid
```

I’d use `sea_` or `seaway_`; since you like shorter IDs, `sea_` is nice.

---

## `name`

Display name.

Examples:

```text
Sable–Thaurin Trade Route
Brooding Sea Crossing
Lost Eastvoid Crossing
Port Sable Approach
```

---

## `seaway_type`

This replaces your current `group` field.

Instead of:

```text
group = seaway
```

Use:

```text
seaway_type
```

Possible values:

```text
trade_route
ferry_route
coastal_route
open_ocean_route
strait_crossing
supply_route
military_route
exploration_route
pilgrimage_route
smuggling_route
```

For Yanorra, I’d especially expect:

```text
trade_route
coastal_route
strait_crossing
supply_route
exploration_route
lost_route
```

---

## `status`

This is the big one.

Recommended values:

```text
active
seasonal
dangerous
restricted
abandoned
lost
theoretical
speculative
historic
closed
unknown
```

I’d define them like this:

```text
active
  Currently used with some regularity.

seasonal
  Only usable during certain Drift/weather/tidal windows.

dangerous
  Technically used, but high-risk.

restricted
  Controlled by a state, navy, guild, port authority, quarantine, etc.

abandoned
  Once used, no longer maintained or attempted.

lost
  Known from records, but exact route is no longer known.

theoretical
  Proposed by navigators/cartographers, but not confirmed by successful passage.

speculative
  Based on rumor, myth, or incomplete accounts.

historic
  Used in the past, especially pre-Drift, but not part of current navigation.

closed
  Officially forbidden or blocked.

unknown
  Status not currently known.
```

Tiny correction: use **`abandoned`**, not `abadoned`, and **`theoretical`**, not `theorhetical`.

---

# `hazard_level`

Keep this separate from `status`.

A route can be:

```text
status = active
hazard_level = extreme
```

That is very Yanorra.

Possible values:

```text
none
low
medium
high
extreme
unknown
```

Examples:

```text
Sable–Thaurin Trade Route
status = active
hazard_level = high

Brooding Sea Crossing
status = active
hazard_level = extreme

Lost Eastvoid Crossing
status = lost
hazard_level = unknown
```

---

# `certainty`

Also separate from `status`.

Possible values:

```text
confirmed
approximate
disputed
speculative
mythic
unknown
```

This is useful because the line geometry itself may be uncertain.

Example:

```text
status = historic
certainty = approximate
```

Meaning: “we believe this route existed, but the exact path is approximate.”

---

# `seasonality`

Useful because Yanorra’s seas are unstable.

Possible values:

```text
year_round
seasonal
rare_window
drift_dependent
unknown
```

Examples:

```text
seasonality = year_round
seasonality = rare_window
seasonality = drift_dependent
```

---

# `traffic_level`

How commonly used the route is.

Possible values:

```text
none
rare
low
medium
high
unknown
```

This lets you distinguish a major trade lane from a dangerous route attempted once per year.

---

# `start_id` and `end_id`

These point to settlements, ports, islands, or regions.

Examples:

```text
start_id = stl_port_sable
end_id   = stl_gate_thaurin
```

For multi-stop routes, you can still use start/end as the main endpoints, and the geometry itself can pass through places like Sabletown.

---

# Recommended final schema

```text
id              Text
name            Text
seaway_type     Text
status          Text
rank            Integer
hazard_level    Text
certainty       Text
seasonality     Text
traffic_level   Text
start_id        Text
end_id          Text
notes           Text
```

For QGIS, I’d make `rank` an integer. Everything else can be text.

---

# Example entries

## Active major trade route

```json
{
  "id": "sea_sable_thaurin",
  "name": "Sable–Thaurin Trade Route",
  "seaway_type": "trade_route",
  "status": "active",
  "rank": 1,
  "hazard_level": "high",
  "certainty": "confirmed",
  "seasonality": "seasonal",
  "traffic_level": "high",
  "start_id": "stl_port_sable",
  "end_id": "stl_gate_thaurin",
  "notes": "Primary Known World route between Duvessa and Velu via Sabletown."
}
```

## Dangerous crossing

```json
{
  "id": "sea_brooding_crossing",
  "name": "Brooding Sea Crossing",
  "seaway_type": "strait_crossing",
  "status": "active",
  "rank": 2,
  "hazard_level": "extreme",
  "certainty": "confirmed",
  "seasonality": "rare_window",
  "traffic_level": "low",
  "start_id": "reg_eanorra",
  "end_id": "reg_wanorra",
  "notes": "Narrow but deadly crossing with very low survival rates."
}
```

## Lost or theoretical route

```json
{
  "id": "sea_lost_eastvoid",
  "name": "Lost Eastvoid Crossing",
  "seaway_type": "exploration_route",
  "status": "lost",
  "rank": 5,
  "hazard_level": "unknown",
  "certainty": "speculative",
  "seasonality": "unknown",
  "traffic_level": "none",
  "start_id": "nat_velu",
  "end_id": "myth_aunqara",
  "notes": "Pre-Drift accounts suggest a possible crossing toward Aunqara, but no confirmed modern route exists."
}
```

## Buildings

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

## Streets

This is for `streets_major.geojson` and `streets_minor.geojson`.

```
id
  Type: Text
  Purpose: Stable unique feature ID
  Examples: street_gunsey_market_lane, street_port_sable_old_quay_road

group
  Type: Text
  Purpose: Broad layer/category grouping; useful if you later merge street layers
  Possible values:
    street
    road
    alley
    path
    service
  Example: street

name
  Type: Text
  Purpose: Display name of the street
  Examples: Market Lane, Old Quay Road, Mill Street
  Note: Leave blank for unnamed minor streets.

settlement_id
  Type: Text
  Purpose: Settlement this street belongs to
  Examples: stl_gunsey, stl_port_sable, stl_sunshine_beach

country_id
  Type: Text
  Purpose: Nation this street belongs to
  Examples: nation_barrel, nation_duvessa, nation_velu

district_id
  Type: Text
  Purpose: Optional district, ward, neighborhood, or quarter
  Examples: dist_port_sable_old_harbor, dist_gunsey_market_square
  Note: Leave blank if the settlement has no districts.

status
  Type: Text
  Purpose: Current condition or usage state
  Possible values:
    active
    damaged
    abandoned
    ruined
    blocked
    under_construction
    planned
    seasonal
    restricted
    unknown

surface
  Type: Text
  Purpose: Main road surface
  Possible values:
    paved
    stone
    cobble
    brick
    gravel
    dirt
    sand
    boardwalk
    mixed
    unknown

access
  Type: Text
  Purpose: Who can normally use the street
  Possible values:
    public
    restricted
    private
    military
    service
    pedestrian
    emergency
    closed
    unknown

bridge
  Type: Boolean
  Purpose: Whether this street segment is a bridge
  Possible values:
    true
    false
  Example: false

tunnel
  Type: Boolean
  Purpose: Whether this street segment is a tunnel
  Possible values:
    true
    false
  Example: false

oneway
  Type: Boolean
  Purpose: Whether traffic moves one direction only
  Possible values:
    true
    false
  Example: false
  Note: Useful if you ever add routing logic, but can be false/blank for most Yanorra maps.

route_id
  Type: Text
  Purpose: Optional shared route ID if this street segment is part of a named route
  Examples: route_port_sable_harbor_loop, route_gunsey_market_road
  Note: Usually blank for ordinary minor streets.

alt_name
  Type: Text
  Purpose: Older, alternate, local, or informal name
  Examples: Old Mill Lane, Fisher’s Cut, North Track

notes
  Type: Text
  Purpose: Freeform notes
  Examples: Narrow residential street leading toward the old mill.
  ```

## Parks Layer

```
id
  Type: Text
  Purpose: Stable unique feature ID
  Examples: park_gunsey_town_green, park_port_sable_old_harbor_green

name
  Type: Text
  Purpose: Display name of the park/open space
  Examples: Town Green, Old Harbor Green, North Garden

settlement_id
  Type: Text
  Purpose: Settlement this park belongs to
  Examples: stl_gunsey, stl_port_sable, stl_sunshine_beach

country_id
  Type: Text
  Purpose: Nation this park belongs to
  Examples: nation_barrel, nation_duvessa, nation_velu

district_id
  Type: Text
  Purpose: Optional district, ward, neighborhood, or quarter
  Examples: dist_port_sable_old_harbor, dist_gunsey_market_square
  Note: Leave blank if the settlement has no districts.

park_type
  Type: Text
  Purpose: Kind of park or urban open space
  Possible values:
    town_green
    garden
    public_park
    plaza_green
    commons
    courtyard
    memorial_park
    temple_garden
    waterfront_park
    playground
    sports_field
    cemetery
    grove
    protected_green
    ruin_park
    private_garden
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
    seasonal
    restricted
    unknown

access
  Type: Text
  Purpose: Who can normally enter/use it
  Possible values:
    public
    restricted
    private
    ceremonial
    government
    military
    staff_only
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
  Examples: park_gunsey_town_green, wiki_old_harbor_green

label_rank
  Type: Integer
  Purpose: Label priority; lower number means more important if you follow the same pattern as buildings
  Examples:
    1 = most important
    2 = important settlement landmark
    3 = local named park
    4 = minor open space

zoom_min
  Type: Integer
  Purpose: Minimum website zoom level where this park appears
  Examples:
    13
    14
    15
    16

notes
  Type: Text
  Purpose: Freeform notes
  Examples: Small public green near the town center.
```