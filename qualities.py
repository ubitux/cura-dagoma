import os
import sys
from xml.etree import ElementTree as ET

from materials import extract_materials
from definition import extract_definition

def _write_ini(out, data):
    for section_name, section_data in data.items():
        out.write('[%s]\n' % section_name)
        for kv in section_data.items():
            out.write('%s = %s\n' % kv)
        out.write('\n')

def extract_qualities(xml_filename):
    qualities_data = {}

    definition_data = extract_definition(xml_filename)

    root = ET.parse(xml_filename)
    qualities = root.find('Bloc_Precision')
    for quality in qualities.findall('Precision'):

        name = quality.attrib['name']
        name_id = name.split(maxsplit=1)[0].lower()
        assert name_id not in ('rapide', 'fin') # french profiles not supported

        name_remap = {'standard': 'normal', 'thin': 'high'}
        name_id = name_remap.get(name_id, name_id)

        fields_map = {
                'speed_print':  'print_speed',
                'speed_travel': 'travel_speed',
                'speed_infill': 'infill_speed',
        }
        values_fields = (
                ('layer_height',        float),
                #solid_layer_thickness                  -> TODO
                ('wall_thickness',      float),
                ('speed_print',         int),           # print_speed
                #temp_preci                             -> TODO
                ('speed_travel',        int),           # travel_speed
                #bottom_layer_speed                     -> TODO
                ('speed_infill',        int),           # infill_speed
                #inset0_speed                           -> TODO
                #insetx_speed                           -> TODO
        )

        values = {}
        for field, field_type in values_fields:
            dagoma_field = fields_map.get(field, field)
            values[field] = field_type(quality.find(dagoma_field).text)

        qualities_data[name_id] = {
                'general': {
                    'version': 2,
                    'name': name,
                    'definition': definition_data['id'],
                },
                'metadata': {
                    'type': 'quality',
                    'quality_type': name_id,
                },
                'values': values,
        }

    return qualities_data

def _write_qualities(xml_filename, out_dir):

    qualities_data  = extract_qualities(xml_filename)
    materials_data  = extract_materials(xml_filename)

    for material_id, material_data in materials_data.items():

        if 'flex' in material_id:
            cfgs = ['flexible']
        elif 'wood' in material_id:
            cfgs = ['wood']
        else:
            cfgs = ['fast', 'normal', 'high']

        for quality_id in cfgs:
            quality_data = qualities_data[quality_id].copy()
            quality_data['metadata']['material'] = material_id
            printer = quality_data['general']['definition'].replace('dagoma_', '')
            filename = '%s_%s_%s.inst.cfg' % (printer, material_id, quality_id)
            filename = os.path.join(out_dir, filename)
            print(filename)
            outf = open(filename, 'w')
            _write_ini(outf, quality_data)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: %s <xml_config.xml> <out_dir>' % sys.argv[0])
        sys.exit(0)
    _write_qualities(*sys.argv[1:])
