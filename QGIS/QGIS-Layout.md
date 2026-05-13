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