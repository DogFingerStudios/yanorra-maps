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
