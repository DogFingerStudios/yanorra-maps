import os
import processing

from pathlib import Path

import qgis.core
import qgis.utils
from qgis.core import QgsProject
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsVectorLayer,
    QgsWkbTypes,
)

_RUNNING = False

def saveProject():
    # rebuild_derived_cell_layers()
    export_data_files()


def openProject():
    layer = QgsProject.instance().mapLayersByName('cells_smooth')[0]
    layer.editingStopped.connect(rebuild_derived_cell_layers)
    
    layer = QgsProject.instance().mapLayersByName('streets_minor')[0]
    layer.editingStopped.connect(generate_street_polygons)

def closeProject():
    pass
    
def rebuild_derived_cell_layers():
    import processing
    from pathlib import Path
    
    global _RUNNING

    if _RUNNING:
        return

    _RUNNING = True

    try:
        project = QgsProject.instance()

        matches = project.mapLayersByName("cells_smooth")
        if not matches:
            print("[Yanorra] Could not find layer: cells_smooth")
            return

        source_layer = matches[0]

        project_dir = Path(project.fileName()).parent
        generated_dir = project_dir / "layers" / "generated"
        generated_dir.mkdir(parents=True, exist_ok=True)

        jobs = [
            ("state", generated_dir / "states.geojson"),
            ("biome", generated_dir / "biomes.geojson"),
            ("height", generated_dir / "height.geojson"),
            ("", generated_dir / "land.geojson")
        ]

        for field, final_path in jobs:
            temp_path = final_path.with_suffix(".tmp.geojson")

            print(f"[Yanorra] Rebuilding {final_path.name} from field: {field}")

            if temp_path.exists():
                temp_path.unlink()

            processing.run(
                "native:dissolve",
                {
                    "INPUT": source_layer,
                    "FIELD": [field],
                    "SEPARATE_DISJOINT": False,
                    "OUTPUT": str(temp_path),
                },
            )

            if final_path.exists():
                final_path.unlink()

            os.replace(str(temp_path), str(final_path))

        print("[Yanorra] Derived cell layers rebuilt.")

    finally:
        _RUNNING = False

def export_data_files():
    import qgis.core
    import qgis.utils

    project_dir = qgis.core.QgsProject.instance().homePath()
    instance = qgis.core.QgsProject.instance()

    output_path = os.path.join(project_dir, 'export', 'StatesData.geojson')
    layers = instance.mapLayersByName('states')
    if layers:
        layer = layers[0]
        qgis.core.QgsVectorFileWriter.writeAsVectorFormat(
            layer, 
            output_path, 
            "utf-8", 
            layer.crs(), 
            "GeoJSON"
        )
        qgis.utils.iface.messageBar().pushMessage("Success", f"Exported to {output_path}", level=0, duration=3)
    else:
        print("States layer not found")
        
    output_path = os.path.join(project_dir, 'export', 'TownsData.geojson')        
    layers = instance.mapLayersByName('Data-Burgs')
    if layers:
        layer = layers[0]
        qgis.core.QgsVectorFileWriter.writeAsVectorFormat(
            layer, 
            output_path, 
            "utf-8", 
            layer.crs(), 
            "GeoJSON"
        )
        qgis.utils.iface.messageBar().pushMessage("Success", f"Exported to {output_path}", level=0, duration=3)
    else:
        print("Data-Burgs layer not found")
        
    output_path = os.path.join(project_dir, 'export', 'BiomesData.geojson')        
    layers = instance.mapLayersByName('biomes')
    if layers:
        layer = layers[0]
        qgis.core.QgsVectorFileWriter.writeAsVectorFormat(
            layer, 
            output_path, 
            "utf-8", 
            layer.crs(), 
            "GeoJSON"
        )
        qgis.utils.iface.messageBar().pushMessage("Success", f"Exported to {output_path}", level=0, duration=3)
    else:
        print("'biomes` layer not found")
        

def generate_street_polygons():
    generate_road_polygons("streets_minor")

def generate_road_polygons(layer_name):
    ROAD_WIDTH_METERS = 9
    BUFFER_DISTANCE_METERS = ROAD_WIDTH_METERS / 2

    OUTPUT_SUFFIX = "_generated"
    FINAL_CRS = QgsCoordinateReferenceSystem("EPSG:4326")

    # ------------------------------------------------------------
    # 1. Find the source LineString layer by name
    # ------------------------------------------------------------

    project = QgsProject.instance()
    matches = project.mapLayersByName(layer_name)

    if not matches:
        raise Exception(f"No layer named '{layer_name}' found in the current QGIS project.")

    source_layer = None

    for candidate in matches:
        if QgsWkbTypes.geometryType(candidate.wkbType()) == QgsWkbTypes.LineGeometry:
            source_layer = candidate
            break

    if source_layer is None:
        raise Exception(f"No source LineString layer named '{layer_name}' found.")

    if not source_layer.isValid():
        raise Exception(f"Source layer '{layer_name}' is not valid.")

    print(f"Loaded source layer: {source_layer.name()}")
    print(f"Feature count: {source_layer.featureCount()}")
    print(f"Source CRS: {source_layer.crs().authid()} - {source_layer.crs().description()}")

    # ------------------------------------------------------------
    # 2. Create a temporary local meter-based CRS
    # ------------------------------------------------------------

    extent = source_layer.extent()
    center = extent.center()

    lon_0 = center.x()
    lat_0 = center.y()

    local_meter_crs = QgsCoordinateReferenceSystem()
    local_meter_crs.createFromProj(
        f"+proj=aeqd "
        f"+lat_0={lat_0} "
        f"+lon_0={lon_0} "
        f"+x_0=0 "
        f"+y_0=0 "
        f"+datum=WGS84 "
        f"+units=m "
        f"+no_defs"
    )

    if not local_meter_crs.isValid():
        raise Exception("Failed to create temporary local meter-based CRS.")

    print(f"Temporary meter CRS centered at lon={lon_0}, lat={lat_0}")

    # ------------------------------------------------------------
    # 3. Reproject source layer to temporary meter CRS
    # ------------------------------------------------------------

    reprojected_lines = processing.run(
        "native:reprojectlayer",
        {
            "INPUT": source_layer,
            "TARGET_CRS": local_meter_crs,
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )["OUTPUT"]

    # ------------------------------------------------------------
    # 4. Buffer by 4.5m to create 9m-wide road polygons
    # ------------------------------------------------------------

    buffered_roads = processing.run(
        "native:buffer",
        {
            "INPUT": reprojected_lines,
            "DISTANCE": BUFFER_DISTANCE_METERS,
            "SEGMENTS": 8,
            "END_CAP_STYLE": 1,   # 0 = round, 1 = flat, 2 = square
            "JOIN_STYLE": 0,      # 0 = round, 1 = miter, 2 = bevel
            "MITER_LIMIT": 2,
            "DISSOLVE": False,
            "SEPARATE_DISJOINT": False,
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )["OUTPUT"]

    # ------------------------------------------------------------
    # 5. Build final and temporary output paths
    # ------------------------------------------------------------

    source_path = source_layer.source().split("|")[0]
    source_file = Path(source_path)

    if not source_file.exists():
        raise Exception(
            f"Could not determine source file path for layer '{layer_name}'. "
            f"Layer source was: {source_layer.source()}"
        )

    generated_dir = source_file.parent / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    output_path = generated_dir / f"{source_file.stem}{OUTPUT_SUFFIX}.geojson"
    temp_output_path = generated_dir / f"{source_file.stem}{OUTPUT_SUFFIX}.tmp.geojson"

    if temp_output_path.exists():
        temp_output_path.unlink()

    # Write to temp first. This avoids writing directly over a GeoJSON
    # that QGIS may still have open, which is especially fragile on Windows.
    processing.run(
        "native:reprojectlayer",
        {
            "INPUT": buffered_roads,
            "TARGET_CRS": FINAL_CRS,
            "OUTPUT": str(temp_output_path),
        },
    )

    # ------------------------------------------------------------
    # 6. Find existing QGIS group urban/generated
    # ------------------------------------------------------------

    root = project.layerTreeRoot()

    urban_group = root.findGroup("urban")

    if urban_group is None:
        raise Exception("Could not find QGIS group: urban")

    generated_group = urban_group.findGroup("generated")

    if generated_group is None:
        raise Exception("Could not find QGIS group: urban/generated")

    # ------------------------------------------------------------
    # 7. Find existing generated layer
    # ------------------------------------------------------------
    # Required QGIS layer tree:
    #
    # urban
    #   generated
    #     streets_minor
    #
    # This function does NOT create the layer in QGIS.
    # It only overwrites the GeoJSON file and reloads the existing layer.

    generated_layer_name = f"{layer_name}{OUTPUT_SUFFIX}"
    existing_generated_layer = None

    for child in generated_group.children():
        if child.layer() and child.layer().name() == generated_layer_name:
            existing_generated_layer = child.layer()
            break

    if existing_generated_layer is None:
        raise Exception(
            f"Could not find existing generated layer: "
            f"urban/generated/{generated_layer_name}"
        )

    # ------------------------------------------------------------
    # 8. Release old datasource, replace file, reload existing layer
    # ------------------------------------------------------------

    # Point the existing layer away from the output file before replacing it.
    # This helps avoid locked-file problems on Windows.
    existing_generated_layer.setDataSource(
        "",
        generated_layer_name,
        "ogr",
    )

    if output_path.exists():
        output_path.unlink()

    os.replace(str(temp_output_path), str(output_path))

    final_output = str(output_path)

    existing_generated_layer.setDataSource(
        final_output,
        generated_layer_name,
        "ogr",
    )
    existing_generated_layer.reload()
    existing_generated_layer.triggerRepaint()

    print(f"Reloaded existing generated layer: urban/generated/{generated_layer_name}")
    print(f"Output path: {final_output}")
    print(f"Polygon feature count: {existing_generated_layer.featureCount()}")

    return final_output