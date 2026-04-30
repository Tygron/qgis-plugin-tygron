OVERLAYS_TYPE = [
    "AREA", "ATTRIBUTE", "AVG", "COMBO", "DISTANCE", "FLOODING", 
    "FUNCTION", "GEO_TIFF", "GROUNDWATER", "HEAT_STRESS", "HEIGHTMAP", 
    "IMAGE", "LIVABILITY", "MUNICIPALITIES", "NEIGHBORHOODS", 
    "NETWORK_DISTANCE", "NETWORK_OVERVIEW", "NETWORK_OWNERSHIP", 
    "OWNERSHIP", "OWNERSHIP_GRID", "RAINFALL", "RESULT_CHILD", 
    "SIGHT_DISTANCE", "SOURCE", "SUBSIDENCE", "TEST", "TRAFFIC_DENSITY", 
    "TRAFFIC_NO2", "TRAFFIC_NOISE", "TRAVEL_DISTANCE", "UNDERGROUND", 
    "VACANCY", "WATERSHED", "WCS", "WMS", "ZIP_CODES", "ZONING"
]
TERRAIN_TYPE = []
FUNCTIONS_TYPE = []

TERRAIN_GROUPS = {
    "Klei": ["klei", "nesvaag", "drechtvaag"],
    "Zand": ["zand", "podzol", "enkeerd"],
    "Veen": ["veen", "moerige", "petgaten"],
    "Water": ["water", "beekdal", "slikvaag"],
    "Infrastructuur": ["bebouwing", "dijk", "weg", "opgespoten"]
}

def get_category(name):
    name = name.lower()
    for cat, keywords in TERRAIN_GROUPS.items():
        if any(key in name for key in keywords):
            return cat
    return "Overig"

def categorize_all_terrains():
    value_map = {f"{item.get('id')} - {item.get('name')}": str(item.get('id')) for item in TERRAIN_TYPE}
   
    indexed_data = {cat: [] for cat in TERRAIN_GROUPS.keys()}
    indexed_data["Overig"] = []

    all_keywords = [key for keys in TERRAIN_GROUPS.values() for key in keys]
    
    for item in value_map:
        item_lower = item.lower()
        found_category = False
        
        for cat, keywords in TERRAIN_GROUPS.items():
            if any(keyword in item_lower for keyword in keywords):
                indexed_data[cat].append(item)
                found_category = True
                break 
        
        if not found_category:
            indexed_data["Overig"].append(item)

    for cat in indexed_data:
        indexed_data[cat].sort()

    return indexed_data

DEFAULT_OVERLAYS = ["SATELLITE","SATELLITE_ORIGINAL","TOPOGRAPHIC","GRAY"]

BUILDING_TYPES = ["BUILDING","ROAD","UNDERGROUND"]
BUILDING_ATTRIBUTE_GROUPING = {
    "Building & Geometry": [
        "DEFAULT_FLOORS",
        "MAX_FLOORS",
        "MIN_FLOORS",
        "FLOOR_HEIGHT_M",
        "HEIGHT",
        "HEIGHT_OFFSET_M",
        "ROOF_COLOR",
        "POPULATION_DENSITY_M2"
    ],
    "Category Weights": [
        "EDUCATION_CATEGORY_WEIGHT",
        "HEALTHCARE_CATEGORY_WEIGHT",
        "LUXE_CATEGORY_WEIGHT",
        "NORMAL_CATEGORY_WEIGHT",
        "OFFICES_CATEGORY_WEIGHT",
        "OTHER_CATEGORY_WEIGHT",
        "SHOPPING_CATEGORY_WEIGHT",
        "SOCIAL_CATEGORY_WEIGHT"
    ],
    "Unit Sizes": [
        "LUXE_UNIT_SIZE_M2",
        "NORMAL_UNIT_SIZE_M2",
        "SOCIAL_UNIT_SIZE_M2"
    ],
    "Traffic": [
        "TRAFFIC_LANES",
        "MAX_SPEED_DYNAMIC",
        "JAM_FACTOR_CARS",
        "JAM_FACTOR_TRUCKS",
        "JAM_FACTOR_VANS",
        "NUM_CARS",
        "NUM_TRUCKS",
        "NUM_VANS",
        "NUM_LIGHT_VEHICLES_DYN"
    ],
    "Infrastructure": [
        "LENGTE",
        "BREEDTEOPENING",
        "HOOGTEOPENING",
        "CULVERT_DIAMETER",
        "KERENDEHOOGTE",
        "HOOGTEBINNENONDERKANTBENEDENSTROOMS",
        "HOOGTEBINNENONDERKANTBOVENSTROOMS",
        "LEFT_SHIELD_HEIGHT",
        "LEFT_TO_SHIELD_DISTANCE",
        "RIGHT_SHIELD_HEIGHT",
        "RIGHT_TO_SHIELD_DISTANCE"
    ],
    "Administration": [
        "BAG_ID",
        "NWB_ID",
        "CONSTRUCTION_FINISH_DATE"
    ]
}

