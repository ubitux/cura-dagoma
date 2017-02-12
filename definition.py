import sys
import json
from xml.etree import ElementTree as ET

def _get_gcode_field(section, field_name):

    # Remap old fields to new ones
    field_map = {
            # old name              new name
            '{print_temperature}': '{material_print_temperature}',
            '{travel_speed}':      '{speed_travel}',
            '{z_offset}':          '0.5', # FIXME
    }

    data = section.find(field_name).text

    lines = []
    for line in data.splitlines():

        # drop comment lines which generally contains deprecated,
        # inexistant variables or unrelated garbage
        line = line.strip()
        if not line or line[0] == ';':
            continue

        # do the old to new variable convert
        for k, v in field_map.items():
            line = line.replace(k, v)

        lines.append(line.strip())

    return {'default_value': '\n'.join(lines)}

def _get_default_dict(xml_node, field_name, field_type=str):
    return {'default_value': field_type(xml_node.find(field_name).text)}

def _extract_fields(dst, section, fields):
    fields_map = {
            # new name                           old name
            'machine_extruder_count':           'extruder_amount',
            'machine_heated_bed':               'has_heated_bed',
            'machine_gcode_flavor':             'gcode_flavor',
            'machine_nozzle_size':              'nozzle_size',
            'cool_fan_enabled':                 'fan_enabled',
            'cool_fan_full_at_height':          'fan_full_height',
            'cool_fan_speed':                   'fan_speed',
            'cool_lift_head':                   'cool_head_lift',
            'cool_min_speed':                   'cool_min_feedrate',
            'skirt_brim_minimal_length':        'skirt_minimal_length',
            'skin_overlap':                     'fill_overlap',
            'support_pattern':                  'support_type',
            'support_infill_rate':              'support_fill_rate',
            'magic_spiralize':                  'spiralize',
            'raft_base_line_width':             'raft_base_linewidth',
            'raft_interface_line_width':        'raft_interface_linewidth',
            'meshfix_union_all':                'fix_horrible_union_all_type_a',
            'meshfix_union_all_remove_holes':   'fix_horrible_union_all_type_b',
            'meshfix_keep_open_polygons':       'fix_horrible_use_open_bits',
            'meshfix_extensive_stitching':      'fix_horrible_extensive_stitching',
    }
    for field, field_type in fields:
        dagoma_field = fields_map.get(field, field)
        dst[field] = _get_default_dict(section, dagoma_field, field_type)

def extract_definition(xmlroot):
    bool_eval = lambda x: eval(x)
    str_lower = lambda x: str(x).lower()

    definition_data = None
    o = {}

    # Machine fields
    for section_name in ('Discovery200', 'DiscoEasy200'):
        section = xmlroot.find(section_name)
        if not section:
            continue

        machine_fields = (
                ('machine_name',            str),
                # machine_type                             -> TODO
                ('machine_width',           int),
                ('machine_depth',           int),
                ('machine_height',          int),
                ('machine_extruder_count',  int),          # extruder_amount
                ('machine_heated_bed',      bool_eval),    # has_heated_bed
                ('machine_center_is_zero',  bool_eval),
                # machine_shape                            -> TODO
                ('machine_nozzle_size',     float),        # nozzle_size
                # extruder_head_size_min_x                 -> polygons, see below
                # extruder_head_size_min_y                 -> polygons, see below
                # extruder_head_size_max_x                 -> polygons, see below
                # extruder_head_size_max_y                 -> polygons, see below
                # extruder_head_size_height                -> TODO
                ('machine_gcode_flavor',    str),          # machine_gcode_flavor
                ('retraction_enable',       bool_eval),
        )
        _extract_fields(o, section, machine_fields)
        min_x = int(section.find('extruder_head_size_min_x').text)
        min_y = int(section.find('extruder_head_size_min_y').text)
        max_x = int(section.find('extruder_head_size_max_x').text)
        max_y = int(section.find('extruder_head_size_max_y').text)
        polygons = ((-min_x, -min_y),
                    (-min_x,  max_y),
                    ( max_x,  max_y),
                    ( max_x, -min_y))
        o['machine_head_with_fans_polygon'] = {'default_value': polygons}

        definition_id = 'dagoma_' + section_name.lower()
        definition_data = {
                'id': definition_id,
                'version': 2,
                'name': 'Dagoma ' + section.find('machine_name').text,
                'inherits': 'fdmprinter',
                'metadata': {
                    'visible': True,
                    'manfacturer': 'Dagoma',
                    'author': 'Clément Bœsch, Delphin PETER',
                    'category': 'Other',
                    'platform': definition_id + '_platform.stl',
                    'file_formats': 'text/x-gcode',
                    'has_machine_quality': True,
                },
                'overrides': o,
        }

    assert definition_data is not None

    # Gcode
    gcode = xmlroot.find('GCODE')
    o['machine_start_gcode'] = _get_gcode_field(gcode, 'Gstart')
    o['machine_end_gcode']   = _get_gcode_field(gcode, 'Gend')

    # Config Adv
    section = xmlroot.find('Config_Adv')
    config_adv_fields = (
            ('retraction_speed',    int),
            ('retraction_amount',   float),
            #bottom_thickness                               -> TODO: belongs in qualities?
            #layer0_width_factor                            -> TODO: belongs in qualities?
            #object_sink                                    -> TODO: belongs in qualities?
            ('cool_min_layer_time', int),
            ('cool_fan_enabled',    bool_eval),             # fan_enabled
    )
    _extract_fields(o, section, config_adv_fields)

    # Config Expert
    section = xmlroot.find('Config_Expert')
    config_expert_fields = (
            ('retraction_min_travel',           float),
            # retraction_combing                            -> TODO: changed type from bool to string
            # retraction_minimal_extrusion                  -> TODO: disabled setting?
            ('retraction_hop',                  int),       # XXX: doesn't retraction_hop_enabled needs to be set?
            ('skirt_line_count',                int),
            ('skirt_gap',                       int),
            ('skirt_brim_minimal_length',       int),       # skirt_minimal_length
            ('cool_fan_full_at_height',         float),     # fan_full_height
            ('cool_fan_speed',                  int),       # fan_speed
            # fan_speed_max                                 -> see cool_fan_speed/maximum_value below
            ('cool_min_speed',                  int),       # cool_min_feedrate
            ('cool_lift_head',                  bool_eval), # cool_head_lift
            # solid_top                                     -> TODO: top_thickness in qualities?
            # solid_bottom                                  -> TODO: bottom_thickness in qualities?
            ('skin_overlap',                    int),       # fill_overlap / FIXME: infill_overlap?
            ('support_pattern',                 str_lower), # support_type
            ('support_angle', int),
            ('support_infill_rate',             int),       # support_fill_rate
            ('support_xy_distance',             float),
            ('support_z_distance',              float),
            ('magic_spiralize',                 bool_eval), # spiralize
            # simple_mode                                   -> TODO
            ('brim_line_count',                 int),
            ('raft_margin',                     int),
            # raft_line_spacing                             -> TODO: which of raft_*_line_spacing?
            ('raft_base_thickness',             float),
            ('raft_base_line_width',            float),     # raft_base_linewidth
            ('raft_interface_thickness',        float),
            ('raft_interface_line_width',       float),     # raft_interface_linewidth
            ('raft_airgap',                     float),
            ('raft_surface_layers',             int),
            ('meshfix_union_all',               bool_eval), # fix_horrible_union_all_type_a
            ('meshfix_union_all_remove_holes',  bool_eval), # fix_horrible_union_all_type_b
            ('meshfix_keep_open_polygons',      bool_eval), # fix_horrible_use_open_bits
            ('meshfix_extensive_stitching',     bool_eval), # fix_horrible_extensive_stitching
    )
    _extract_fields(o, section, config_expert_fields)
    o['cool_fan_speed']['maximum_value'] = section.find('fan_speed_max').text # expression, left as string

    return definition_data

def _write_definition(xml_filename, output_filename):
    xmlroot = ET.parse(xml_filename)
    definition_data = extract_definition(xmlroot)
    json_data = json.dumps(definition_data, indent=4) + '\n'
    open(output_filename, 'w').write(json_data)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: %s <xml_config.xml> <output.json>' % sys.argv[0])
        sys.exit(0)
    _write_definition(*sys.argv[1:])
