# © 2024 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
leak_shield_headline = '''                                                                                                    
        .:=*.                                                                          .--.         
         ..=*-..                                                                    ..-+--.         
           .=%+=.                                                                  .=*#-            
            .:#%==.                                                              .==%#:.            
              .*%*+:                          ...:-..                          .:+*%+.              
                :##+=.     .:-++++-.        .....:----..        .-====-.      :++%*.                
                 .-%#+-..=*+:....-:.      .....:========-.      .--...:=#+:..=+#%-.                 
                   .*%*##+-.          ...:::::--===++++++*+:..          .=*#**%=                    
                    .+#**+..      ..:-=-::::----===++++******+-..       .:**##-.                    
                  .-#+=*+-::..:-=+**#+=-:::::---===++++**********+==-:..::-*++*+.                   
                 .=*...:-:::-==+**+=---::::::---===++++********==+*###**+=-:-:.:#:                  
                .-+.  .::-++**++===---:::::::---===++++*********++===+++**=-::  :*.                 
                .+-.  .::=***+++===----::::::---===++++*********++====++**=:-.  .+-.                
                .**.  .::-***+++===----::::::---===++++*********++====++**-:-.  -#=.                
                 ..   .::-***+++===----::::::---===+++**********+++==+++**-:-   ...                 
                      .:::+**+++===----::::::---===+++**********+++=++++*+-::                       
                       .::+**+++===----::::::---===+++***********+++++++*+--.                       
                       .::=**+++===----::::::---===+++***********+++++++*=--                        
                        :::**+++===----::::::---===+++***********++++++++==.                        
                        .::=*+++===----:::::----==+++************++++++*+=-.                        
     _        _______  _______  _          _______          _________ _______  _        ______  
    ( \      (  ____ \(  ___  )| \    /\  (  ____ \|\     /|\__   __/(  ____ \( \      (  __  \ 
    | (      | (    \/| (   ) ||  \  / /  | (    \/| )   ( |   ) (   | (    \/| (      | (  \  )
    | |      | (__    | (___) ||  (_/ /   | (_____ | (___) |   | |   | (__    | |      | |   ) |
    | |      |  __)   |  ___  ||   _ (    (_____  )|  ___  |   | |   |  __)   | |      | |   | |
    | |      | (      | (   ) ||  ( \ \         ) || (   ) |   | |   | (      | |      | |   ) |
    | (____/\| (____/\| )   ( ||  /  \ \  /\____) || )   ( |___) (___| (____/\| (____/\| (__/  )
    (_______/(_______/|/     \||_/    \/  \_______)|/     \|\_______/(_______/(_______/(______/                              
                              .=**+=----::::---==+++************++#*.                               
                               .=**=----:::----==+++***********++#*.                                
                                .=**=---:::---===+++**********+*#+:.                                
                                 .=*+=--:::---===+++**********+**.                                  
                                ..:=*+=-:::---==++++*******#***+:..                                 
                               ..::==+=-------==++++**********==-::.                                
                              .::-=...--::----==++++*********-..:=-::.                              
                            .::-=-.   .::::--===++++*******+.    .==::..                            
                          ..::=-.       .::::===++++***+++-.       :=-::.                           
                        ..::-=:.         ..:::-=++++*+=++:.         .-=-:..                         
                        .:-=:              .....-++--==:              .==::.                        
                     ..::--.                .....----:.                 .=-::.                      
                    ..:--..                    ..::.                     .:=-:..                    
                   .:-=..                                                  .:=:.                    
                 ..:-:.                                                      .:-..                  
                 ...                                                            ...      

© 2024 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
Author: Dario Amadori 
Version: 1.0a
'''
import os
import sys
import ansys.meshing.prime as prime
import time
import logging
import json
import ansys.fluent.core as pyfluent 


meshing = pyfluent.session_meshing.Meshing

# os.environ['AWP_ROOT242'] = '/apps/ansys_inc/preview/v242_Certified_Daily/ansys_inc/v242/'
# os.environ['FLUENT_PYFLUENT_ROOT'] = '/home/damadori/.virtualenvs/pyansys241/lib/python3.10/site-packages'
# sys.path.append(os.path.join(os.environ['AWP_ROOT242'],'meshing/site'))
# sys.path.append('/home/damadori/LeakShield')
# sys.path.append('/home/damadori/.virtualenvs/pyansys241/lib/python3.10/site-packages/')
# sys.path.remove('/home/damadori/.local/lib/python3.10/site-packages')
### __import__('__main__').meshing = meshing
### __import__('__main__').leakshield_database_filepath = leakshield_database_filepath

global leak_shield_database
global prime_client, model, file_io, mesh_util_lucid

# define a non-floating path to a leakshield database (will be overwritten if a sysargv is found)
global leakshield_database_filepath
# leakshield_database_filepath = '/home/fkatsoul/VWheadlamp/headlamp_LS.json'
# leakshield_database_filepath = '/lus01/damadori/Volvo/EX90_variant1/leak_shield_settings_EX90.json'
# leakshield_database_filepath = '/home/damadori/LeakShield/drivaer_leakshield_example/drivaer_leakshield_example.json'
# leakshield_database_filepath = '/lus01/damadori/endocardium/endocardium_leakshield.json'
# checking for leakshield database file passed as system argv
# print(sys.argv)

if len(sys.argv) == 2:
    leakshield_database_filepath = sys.argv[1]
# else:
#     print('Input JSON not provided.')
#     sys.exit()

# os.chdir(os.path.dirname(leakshield_database_filepath))

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    # handlers=[
        # logging.FileHandler("LeakShield_v.log"),
        # logging.StreamHandler(),
        # ],
    datefmt="%d/%m/%Y %I:%M:%S %p",
)

if __name__ == 'main':
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("LeakShield_v.log"),
            logging.StreamHandler(),
            ],
        datefmt="%d/%m/%Y %I:%M:%S %p",
        )

logging.basicConfig(format="%(message)s")
logging.info(leak_shield_headline)
logging.basicConfig(format="[%(levelname)s] %(message)s")

# try:
#     # load leak_shield_settings
#     logging.info('Loading Leak Shield Settings...')
#     with open(leakshield_database_filepath, "r") as file: 
#         leak_shield_database = json.load(file) 
#     logging.info('Done.')
# except Exception as e:
#     logging.error(f'Reading LeakShield database file failed with following error:\n{e}\nLeakShield will stop.')
#     sys.exit()
   
def load_json_file(leakshield_database_filepath):
    try:
        # load leak_shield_settings
        logging.info('Loading Leak Shield Settings...')
        with open(leakshield_database_filepath, "r") as file: 
            leak_shield_database = json.load(file) 
        logging.info('Done.')
        return leak_shield_database
    except Exception as e:
        logging.error(f'Reading LeakShield database file failed with following error:\n{e}')
        if __name__ == 'main':
            sys.exit()

def initialize_pyprime(leak_shield_database):
    try:
        # client & I/O utilities
        prime_client = prime.launch_prime()
        model = prime_client.model
        file_io = prime.FileIO(model=model)
        mesh_util_lucid = prime.lucid.Mesh(model)

        # Attach logger to PyPrimeMesh model and set logging level
        # model.python_logger.setLevel(logging.WARNING)
        # model.python_logger.addHandler(logging.StreamHandler())

        # Path files - please disregard this block
        logging.info('Initializing paths...')
        cwd = os.getcwd()
        raw_cad_d = os.path.join(leak_shield_database['working_directory'],'raw_cad')
        raw_cad_filenames = [] # next(os.walk(raw_cad_d))[2]

        # load leak_shield_settings
        # logging.info('Loading Leak Shield Settings...')
        # with open(leakshield_database_filepath, "r") as file: 
        #     leak_shield_database = json.load(file)
        return prime_client, model, file_io, mesh_util_lucid
    except Exception as e:
        logging.error(f'PyPrime initialization failed with following error:\n{e}\nLeakShield will stop.')
        if __name__ == 'main':
            sys.exit()

# API for global sizing
def update_global_sizing(min_size:float, max_size:float):
    '''Defines curvature sizing globally for all geometry parts, with a refinement normal angle of 15.0 deg.
    
    Parameters
    ----------
    min_size : float
        minimum size achievable by the refinement. Should be smaller than max_size
    min_size : float
        maximum size achievable by the refinement. Should be bigger than min_size
    ---------
    '''
    model.set_global_sizing_params(prime.GlobalSizingParams(model=model, min=min_size, max=max_size, growth_rate=1.2))
    size_control = model.control_data.create_size_control(sizing_type=prime.SizingType.CURVATURE)
    size_control.set_curvature_sizing_params(prime.CurvatureSizingParams(model=model,min=min_size, max=max_size, normal_angle=15.0))
    size_control.set_suggested_name("curv_global")
    size_control.set_scope(prime.ScopeDefinition(model=model, part_expression="*"))
    return size_control

# API for local sizing
def add_curvature_sizing(min_size:float, normal_angle:float, max_size:float, part_expression:str = '*', label_expression:str ='*', zone_expression:str ='*'):
    '''Defines curvature sizing locally for given scope parts, labels, zones, with a refinement normal angle of 15.0 deg.
    
    Parameters
    ----------
    min_size : float
        minimum size achievable by the refinement. Should be smaller than max_size
    min_size : float
        maximum size achievable by the refinement. Should be bigger than min_size
    part_expression: str
        expression of the scoped parts.
    label_expression: str
        expression of the scoped labels.
    zone_expression: str
        expression of the scoped zones.
    ---------
    '''
    size_control = model.control_data.create_size_control(sizing_type=prime.SizingType.CURVATURE)
    size_control.set_curvature_sizing_params(prime.CurvatureSizingParams(model=model,min=min_size, max=max_size, normal_angle=normal_angle))
    size_control.set_suggested_name(f"curv_local_{min_size}|{max_size}_{part_expression}|{label_expression}|{zone_expression}")
    size_control.set_scope(prime.ScopeDefinition(model=model, part_expression=part_expression, label_expression=label_expression, zone_expression=zone_expression))
    return size_control

# API for local proximity sizing
def add_proximity_sizing(min:float, max:float, elements_per_gap:int, part_expression:str = '*', label_expression:str ='*', zone_expression:str ='*'):
    '''Defines proximity sizing locally for given scope parts, labels, zones.
    
    Parameters
    ----------
    min_size : float
        minimum size achievable by the refinement. Should be smaller than max_size
    min_size : float
        maximum size achievable by the refinement. Should be bigger than min_size
    elements_per_gap : int
        number of elements per gap between parts
    part_expression: str
        expression of the scoped parts.
    label_expression: str
        expression of the scoped labels.
    zone_expression: str
        expression of the scoped zones.
    ---------
    '''
    size_control = model.control_data.create_size_control(sizing_type=prime.SizingType.PROXIMITY)
    size_control.set_suggested_name(f"prox_local_{min}|{max}_{part_expression}|{label_expression}|{zone_expression}")
    size_control.set_proximity_sizing_params(prime.ProximitySizingParams(model=model, min=min, max=max,elements_per_gap=elements_per_gap))
    size_control.set_scope(prime.ScopeDefinition(model=model, part_expression=part_expression, label_expression=label_expression, zone_expression=zone_expression))
    return size_control


# API to regroup imported parts into sub-assemblies
def create_sub_assemblies_and_scope_strings(sub_assemblies_files_dict: dict):
    '''Reorganizes the geometry parts (i.e. mesh objects in Fluent Meshing) and lables based on the given sub-assemblies dictionary
    
    Parameters
    ----------
    sub_assemblies_files_dict : dict[list[str]] 
        dictionary of lists of string, where each key represents a sub-assembly and 
        each item is a list of the corresponding raw CAD files
    Returns
    -------
    sub_assemblies_scope_strings_dict : dict[str]
        a dictionary of all sub-assemblies formatted as prime scope strings
    '''
    
    def file_list_to_scope_string(file_list):
        '''Given a list of filenames, it returns the respective string to give all of them as prime scope
        
        Parameters
        ----------
        file_list : list[str] 
            list of string, each of them being a filename
        Returns
        -------
        str 
            a formatted string of all files as prime scope
        '''
        
        # return "*,".join([file_name[:-4] for file_name in file_list]).lower().replace(' ','_')
        return "*,".join([file_name[:-4] for file_name in file_list])
    
    sub_assemblies_scope_strings_dict = {}
    for k in sub_assemblies_files_dict.keys():
        part_ids = []
        for file in sub_assemblies_files_dict[k]:
            part_ids.append(model.get_part_by_name(file[:-3].lower().replace(' ','_')).id)
        model.merge_parts(part_ids=part_ids, params=prime.MergePartsParams(model=model, merged_part_suggested_name=k))
        sub_assemblies_scope_strings_dict[k] = file_list_to_scope_string(sub_assemblies_files_dict[k])
    return sub_assemblies_scope_strings_dict

# API to add label to face zonelets
def add_label_to_face_zonelets_of_name_pattern(label : str, face_zonelets_name_pattern : str):
    '''
    Adds a given label to the face_zonelets of a given face_zonelets pattern.

    Params:
        label: str
            label to assign to the face zonelet(s)
        face_zonelets_name_patterm: str
            Name pattern of the face zonelet(s) to look for
    '''
    face_zonelets = []
    for part in model.parts:
        face_zonelets.extend(part.get_face_zonelets_of_zone_name_pattern(zone_name_pattern=face_zonelets_name_pattern,name_pattern_params= prime.NamePatternParams(model=model,)))
    for part in model.parts:
        part.add_labels_on_zonelets(labels=[label],zonelets = face_zonelets)

def add_sub_assemblies_labels_to_parts(sub_assemblies_files_dict: dict):
    '''Reorganizes the geometry parts (i.e. mesh objects in Fluent Meshing) and lables based on the given sub-assemblies dictionary
    
    Parameters
    ----------
    sub_assemblies_files_dict : dict[list[str]] 
        dictionary of lists of string, where each key represents a sub-assembly and 
        each item is a list of the corresponding raw CAD files
    Returns
    -------
    sub_assemblies_scope_strings_dict : dict[str]
        a dictionary of all sub-assemblies formatted as prime scope strings
    '''
        
    for sub_assembly in sub_assemblies_files_dict.keys():
        list_of_sub_assemblies_part = []
        for geometry_file_name in sub_assemblies_files_dict[sub_assembly]:
            list_of_sub_assemblies_part.append(geometry_file_name.split('.')[0].lower().replace(' ','_'))
        
        for part_name in list_of_sub_assemblies_part:
            part = model.get_part_by_name(part_name)
            part_face_zonelets = part.get_face_zonelets()   
            part.add_labels_on_zonelets(labels=[sub_assembly],zonelets = part_face_zonelets)
            

def import_and_sort_geometry(sub_assemblies_files_dict: dict):
    '''Manages import of geometry: imports already sorted and labeled geomerty if present,
    otherwise it imports raw CAD files and sorts/labels them, based on the sub-assemblies 
    defined in the LeakShield JSON
    
    Parameters
    ----------
    sub_assemblies_files_dict : dict[list[str]] 
        dictionary of lists of string, where each key represents a sub-assembly and 
        each item is a list of the corresponding raw CAD files
    Returns
    -------
    '''
    # Attempt to import sorted and labeled geometry, if present
    try:
        tic = time.time()
        input_filepath = os.path.join(leak_shield_database['working_directory'],leak_shield_database['input_filename'])
        logging.info(f'Trying to load {input_filepath}...')
        mesh_util_lucid.read(input_filepath)
        toc = time.time()
        logging.info(f'Import time: {(toc - tic)/60:.2f} minutes.\n') 
    except Exception as e:
        logging.info(f'{input_filepath} not found, trying to import raw CAD files.')
        tic = time.time()
        for sub_assembly in sub_assemblies_files_dict.keys():
            for file_name in sub_assemblies_files_dict[sub_assembly]:
                try:
                    input_filepath = os.path.join(leak_shield_database['working_directory'],'raw_cad',leak_shield_database['input_filename'])
                    logging.info(f'Loading {file_name}...')
                    file_io.import_fluent_meshing_meshes(file_names=[os.path.join(raw_cad_d,file_name)], import_fluent_meshing_mesh_params=prime.ImportFluentMeshingMeshParams(model=model,append=True))
                    logging.info('Done.')
                except Exception as e:
                    logging.info(f'{file_name} import failed with following error:\n{e}')
        toc = time.time()
        logging.info(f'Import time: {(toc - tic)/60:.2f} minutes.\n') 
        logging.info('Creating labels for sub-assemblies...')
        for part in model.parts:
            for key in leak_shield_database['sub_assemblies']:
                list_of_sub_assemblies_part = []
                for geometry_file_name in sub_assemblies_files_dict[key]:
                    # geom parts inherit the filename, with some replacements and without file extension
                    list_of_sub_assemblies_part.append(geometry_file_name.split('.')[0].replace(' ','_'))
                if part.name in list_of_sub_assemblies_part:
                    part.add_labels_on_zonelets(labels = [key], zonelets = part.get_face_zonelets())
        logging.info(f'Writing sorted & labeled {input_filepath} to disk...')
        mesh_util_lucid.write(os.path.join(leak_shield_database['working_directory'],leak_shield_database['input_filename']))
        # file_io.write_pmdat(file_name=os.path.join(leak_shield_database['working_directory'],leak_shield_database['input_filename']), file_write_params=prime.FileWriteParams(model=model))
        logging.info('Done.\n')


def add_debug_labels():
    '''
    Checks for quad faces (not supported by wrapper) and converts them into triangles

    Parameters
    ----------
    Returns
    ------
    '''
    pass



def triangulate_quads():
    '''
    Checks for quad faces (not supported by wrapper) and converts them into triangles

    Parameters
    ----------
    Returns
    -------    
    '''
    logging.info(f'Checking for quad faces...')
    nb_triangulated_quads = 0
    for part in model.parts:
        part_summary_res = part.get_summary(prime.PartSummaryParams(model = model, print_id = False, print_mesh = False))
        if part_summary_res.n_quad_faces > 0:
            nb_triangulated_quads += part_summary_res.n_quad_faces
            logging.info(f'{part.name} contains {part_summary_res.n_quad_faces} quad faces, triangulating them...')
            tic = time.time()
            face_zonelets = part.get_face_zonelets() 
            triangulate_params = prime.TriangulateParams()
            surfutils = prime.SurfaceUtilities(model)
            res_triangulate = surfutils.triangulate_face_zonelets(face_zonelets, triangulate_params)
            toc = time.time()
            logging.info(f'Done. Triangulation time: {(toc - tic)/60:.3f} minutes.\n')
    logging.info(f'Quad faces check done. A total of {nb_triangulated_quads} quad faces were triangulated.')

def create_bounding_box(bb_name: str, xmin: float, ymin: float, zmin: float, xmax: float, ymax: float, zmax: float):
    '''
    Creates bounding box

    Parameters
    ----------
    bb_name: name to assign to the bounding box
    xmin... zmax : float
        coordinates of min and max corners of the bounding box
    Returns
    -------    
    '''
    try:
        logging.info(f'Creating bounding box...')
        bbox = prime.BoundingBox(model = model, xmin = xmin, ymin = ymin, zmin = zmin, xmax = xmax, ymax = ymax, zmax = zmax )

        surf = prime.SurfaceUtilities(model = model)
        bb_name = bb_name
        command_name = "PrimeMesh::SurfaceUtilities/CreateBox"
        args = {"box_extents" : bbox._jsonify(), "params" : {"suggestedPartName" : bb_name}}
        res = surf._comm.serve(surf._model, command_name, surf._object_id, args = args)
        model._sync_up_model()
        logging.info(f'Creating zones from labels...')
        for label in model.get_part_by_name(bb_name).get_labels():
            mesh_util_lucid.create_zones_from_labels(label_expression=label)
        logging.info(f'Done.')
    except Exception as e:
        logging.info(f'Bounding box creations failed with following eror: {e}')

def create_contact_patches(wheels_name_pattern: str, ground_name_pattern: str):
    '''
    Creates contact patches between wheels and ground

    Parameters
    ----------
    wheels_name_pattern : str
        pattern of the name of wheels face zonelets
    ground_name_pattern : str
        pattern of the name of ground face zonelets
    Returns
    -------    
    '''
    try:
        logging.info(f'Creating contact patches...')
        wheels_zonelets = []
        for part in model.parts:
            wheels_zonelets.extend(part.get_face_zonelets_of_zone_name_pattern(zone_name_pattern=wheels_name_pattern,name_pattern_params= prime.NamePatternParams(model=model,))) 
        ground_zonelets = []
        for part in model.parts:
            ground_zonelets.extend(part.get_face_zonelets_of_zone_name_pattern(zone_name_pattern=ground_name_pattern,name_pattern_params= prime.NamePatternParams(model=model,))) 
        logging.info(f'Found {len(wheels_zonelets)} facelets for wheel and {len(ground_zonelets)} for ground.')
        if len(wheels_zonelets)==0 or len(ground_zonelets)==0:
            logging.info(f'Contact patches creation will be skipped.')
        else:
            params = prime.CreateContactPatchParams(model,contact_patch_axis= prime.ContactPatchAxis.Z, offset_distance=10.0, suggested_part_name="contact_patch")
            surf = prime.SurfaceUtilities(model = model)
            res = surf.create_contact_patch(wheels_zonelets, ground_zonelets, params = params)
            for label in model.get_part_by_name('contact_patch').get_labels():
                mesh_util_lucid.create_zones_from_labels(label_expression=label)
            logging.info(f'Done.')
    except Exception as e:
        logging.info(f'Contact patches creation failed with following eror: {e}')

def create_leak_shield(leak_shield_settings : dict):
    '''
    Creates internal wrap of scoped geometry with given sizing & leakage prevention settings.
    1 LeakShield Scope is defined
    2 Live & dead points are created (with inverted nature w.r.t. json file)
    3 Wrap controls are defined
    4 For each dead point of the json file:
        - Dead regions are defined
        - prime.wrapper.patch_flow_region is launched

    
    Parameters
    ----------
    leak_shield_settings : dict 
        dictionary of scope, sizing & leakage prevention settings for the leak shield
    Returns
    -------
    '''
    try: 

        tic0 = time.time()
        # Define global and local sizings for wrap
        logging.info(f'-'*int(len(f'|Generating Leak Shield "{leak_shield_settings["name"]}"')))
        logging.info(f'|Generating Leak Shield "{leak_shield_settings["name"]}"|')
        logging.info(f'-'*int(len(f'|Generating Leak Shield "{leak_shield_settings["name"]}"')))
        if leak_shield_settings['zone_expression'] == '*':
            evaluation_type = prime.ScopeEvaluationType.LABELS
        else:
            evaluation_type = prime.ScopeEvaluationType.ZONES
        leak_shield_geometry_scope = prime.ScopeDefinition(
            model            = model, 
            part_expression  = leak_shield_settings['part_expression'], 
            label_expression = leak_shield_settings['label_expression'], 
            zone_expression  = leak_shield_settings['zone_expression'], 
            entity_type      = prime.ScopeEntity.FACEZONELETS,
            evaluation_type  = evaluation_type
            )

        # initialize size lists
        size_control_ids = []
        size_field_ids = []

        # Define global leak shield sizing
        # global_leak_shield_sizing = update_local_sizing(
        #     min_size         = leak_shield_settings['global_leak_shield_sizing']['min_size'], 
        #     max_size         = leak_shield_settings['global_leak_shield_sizing']['max_size'], 
        #     part_expression  = leak_shield_settings['part_expression'], 
        #     label_expression = leak_shield_settings['label_expression'],
        #     zone_expression  = leak_shield_settings['zone_expression'])
        # size_control_ids.append(global_leak_shield_sizing.id)

        # Define dead material points
        logging.info(f'Defining dead material points...')
        dead_material_points = []
        for dmp_name, dmp_coordinates in leak_shield_settings['live_material_points'].items():
            model.material_point_data.create_material_point(
                suggested_name='dmp_'+dmp_name, 
                coords=dmp_coordinates, 
                params=prime.CreateMaterialPointParams( model=model, type=prime.MaterialPointType.DEAD),)
            dead_material_points.append('dmp_'+dmp_name)

        # Define live material points
        logging.info(f'Defining live material points...')
        live_material_points = []
        for lmp_name, dmp_coordinates in leak_shield_settings['dead_material_points'].items():
            model.material_point_data.create_material_point(
                suggested_name='lmp_'+lmp_name, 
                coords=dmp_coordinates, 
                params=prime.CreateMaterialPointParams( model=model, type=prime.MaterialPointType.LIVE),)
            live_material_points.append('lmp_'+lmp_name)

        # Define wrap controls
        logging.info(f'Defining dead region control...')
        faces = model.control_data.get_scope_face_zonelets(scope= leak_shield_geometry_scope, params=prime.ScopeZoneletParams(model)) 

        # Create wrapper and perform wrapping operation
        logging.info(f'LeakShield contains {len(live_material_points)} dead material points: {", ".join([lmp[4:] for lmp in live_material_points])}. wrap operation will be peformed for each of them.')
        
        for lmp in live_material_points:
            logging.info(f'Generating LeakShield wrap for dead zone {lmp[4:]}...')
            leak_shield_dead_region = prime.DeadRegion(
                model=model, 
                face_zonelet_ids=faces,dead_material_points=dead_material_points, 
                hole_size=leak_shield_settings['max_leak_size'])
            leak_shield_patch_params = prime.WrapperPatchFlowRegionsParams(
                model=model, 
                base_size=leak_shield_settings['min_leak_size'], 
                suggested_part_name=f"{leak_shield_settings['name']}::leak_shield_from_{lmp[4:]}", 
                dead_regions=[leak_shield_dead_region], 
                number_of_threads=32)
            wrapper = prime.Wrapper(model=model)
            start = time.time()
            patch_result = wrapper.patch_flow_regions(live_material_point=lmp, params=leak_shield_patch_params)
            end = time.time()
            logging.info(f'LeakShield wrap generation time: {(end - start)/60:.2f} minutes.') 

        logging.info(f'Cleaning material points from model.')
        for lmp in leak_shield_settings['live_material_points'].keys():
            model.material_point_data.delete_material_point('dmp_'+lmp)
        for dmp in leak_shield_settings['dead_material_points'].keys():
            model.material_point_data.delete_material_point('lmp_'+dmp)

        logging.info(f'LeakShield total generation time: {(end - tic0)/60:.2f} minutes.\n') 

    except Exception as e:
        logging.error(f'Leak Shield generation failed with following error: {e}')
        logging.info(f'Cleaning material points from model.')
        for lmp in leak_shield_settings['live_material_points'].keys():
            model.material_point_data.delete_material_point('dmp_'+lmp)
        for dmp in leak_shield_settings['dead_material_points'].keys():
            model.material_point_data.delete_material_point('lmp_'+dmp)



# mesh_util_lucid.read(os.path.join(leak_shield_database['working_directory'], leak_shield_database['input_filename']))

# file_io.read_pmdat(file_name=leak_shield_database['input_filename'], file_read_params=prime.FileReadParams(model=model))

def create():
    '''
    Function that uses previously defined methods/tools to generate LeakShields based on JSON input information.
    '''

    global leak_shield_database
    global prime_client, model, file_io, mesh_util_lucid

    leak_shield_database = load_json_file(leakshield_database_filepath)

    print('11111'+leakshield_database_filepath)

    print(leak_shield_database)

    initialize_pyprime(leak_shield_database)

    prime_client, model, file_io, mesh_util_lucid = initialize_pyprime(leak_shield_database)

    print(2)

    import_and_sort_geometry(leak_shield_database['sub_assemblies'])

    triangulate_quads()

    for key in leak_shield_database['leak_shields'].keys():
        create_leak_shield(leak_shield_database['leak_shields'][key])

    if leak_shield_database['bounding_box']['create?'] == 'True':
        create_bounding_box(**leak_shield_database['bounding_box']['values'])

    if leak_shield_database['contact_patches']['create?'] == 'True':
        create_contact_patches(**leak_shield_database['contact_patches']['values'])

def save():
    '''
    Function that saves the output based on options given in JSON file.
    '''

    if leak_shield_database['save_input+leakshields?'] == 'True':
        mesh_util_lucid.write(os.path.join(leak_shield_database['working_directory'], leak_shield_database['input_filename'].split('.')[0]+'+leak_shields.msh.gz'))

    if leak_shield_database['save_leakshields_only?'] == 'True':
        to_delete = []
        for part in model.parts:
            if '::leak_shield_from_' not in part.name:
                to_delete.append(part.id)
        model.delete_parts(to_delete)
        mesh_util_lucid.write(os.path.join(leak_shield_database['working_directory'], leak_shield_database['input_filename'].split('.')[0]+'_leak_shields_only.msh.gz'))
    
    prime_client.exit()


def main():
    create()
    save()

if __name__ == "__main__":
    main()
else:
    logging.warning(f'LeakShield has been called by another application. Please define the "leakshield_database_filepath" variable (pointing at the location of your JSON file) before proceeding with LeakShield.')
    meshing = __import__('__main__').meshing
    leakshield_database_filepath = __import__('__main__').leakshield_database_filepath

# model.parts[6].remove_labels_from_zonelets(labels=['front_grill'],zonelets=model.parts[6].get_face_zonelets())
# add_label_to_face_zonelets_of_name_pattern(label='front_frame_vane', face_zonelets_name_pattern='fc00aaw93558_005-frame,fc00aaw93560_001-slave_vane_*,fc00aaw93563_002-drive_vane_*, fc00aaw93561_001-slave_vane_*, fc00aaw93562_002-drive_vane_*, fc00aaw44151_013-plinth-_non_camera-_big_horn_laramie*, fc00aax54849_002-link*, fc00aax52383_002-foam_vertical*, fc00abs61022_001-actuator_active_grille_shutter*, fc00aai57641_002-actuator_pin*')
# add_label_to_face_zonelets_of_name_pattern(label='front_grill', face_zonelets_name_pattern="fc00aav85109_008-big_horn_painted_billets*, fc00aav85108_017-texture_carrier_-_laramie_big_horn*, fc00aaw44151_013-plinth-_non_camera-_big_horn_laramie.2, fc00aax48084_004-base_carrier_hardware_kit__part_sheets")

class debug_toolbox():
    
    '''
    Set of functions for debugging and manual usage of LeakShield inside Fluent Meshing PyConsole
    '''

    def reload_json_file():
        '''
        Reloads the settings JSON file.
        It can be used if one wants to change settings and re-try
        '''
        try:
            logging.info('Reloading Leak Shield Settings...')
            with open(leakshield_database_filepath, "r") as file: 
                leak_shield_database = json.load(file) 
            logging.info('Done.')
            # return leak_shield_database
        except Exception as e:
            logging.error(f'Reading LeakShield database file failed with following error:\n{e}\n Check if the global variable "leakshield_database_filepath" is defined.')
    
    def create_and_read_results():
        '''
        Launches LeakShield generation and then inports its output in Fluent Meshing
        '''
        create()

        generated_file_path = os.path.join(leak_shield_database['working_directory'], leak_shield_database['input_filename'].split('.')[0]+'+leak_shields.msh.gz')
        mesh_util_lucid.write(generated_file_path)

        try:
            meshing.tui.file.read_mesh(f'"{generated_file_path}"')        
        except Exception as e:
            logging.error(f'Reading LeakShield output file failed with following error:\n{e}')

    def recreate_and_update_results(keep_existing_patches=False):
        '''
        Launches LeakShield generation saving the patches only and then appends them in Fluent Meshing
        '''

        def delete_mesh_object(obj_name):
            try:
                logging.info(f'Trying to remove mesh object {obj_name}...')
                meshing.tui.objects.delete(f'("{obj_name}")', 'yes')
                logging.info(f'{obj_name} removed.')
            except Exception as e:
                logging.error(f'{e}')

        create()

        to_delete = []
        for part in model.parts:
            if '::leak_shield_from_' not in part.name:
                to_delete.append(part.id)
        model.delete_parts(to_delete)
        mesh_util_lucid.write(os.path.join(leak_shield_database['working_directory'], leak_shield_database['input_filename'].split('.')[0]+'_leak_shields_only.msh.gz'))

        logging.info(f'Trying to remove mesh objects corresponding to newly created patches, to avoid duplicates.')
        part_names = [part.name for part in model.parts]
        logging.info(f'Newly created patches objects: {part_names}')
        if keep_existing_patches == False:
            for part_name in part_names:
                if part_name in meshing.meshing_utilities.get_all_objects():
                    logging.info(f'{part_name} already present in model, it will be overwritten.')
                    delete_mesh_object(part_name)   

        try:
            meshing.tui.file.append_mesh(os.path.join(leak_shield_database['working_directory'], leak_shield_database['input_filename'].split('.')[0]+'_leak_shields_only.msh.gz'))      
        except Exception as e:
            logging.error(f'Reading LeakShield output file failed with following error:\n{e}')

    def show_faces_of_label(label: str):
        '''
        Shows on screen all face zone(let)s of the given label
        '''
        meshing.scheme_eval.scheme_eval(f'''(define {label}-faces      (tgapi-util-get-face-zone-id-list-with-labels (get-face-zones-of-filter '*) (list "{label}")))''')
        meshing.tui.display.draw_zones(f"(eval-expr '{label}-faces)")
