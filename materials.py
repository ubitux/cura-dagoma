import os
import sys
from xml.etree import ElementTree as ET

def _write_xml(filename, brand, diameter, temp, material, color, density):
    xml_root       = ET.Element('fdmmaterial', xmlns='http://www.ultimaker.com/material')
    xml_metadata   = ET.SubElement(xml_root, 'metadata')
    xml_properties = ET.SubElement(xml_root, 'properties')
    xml_settings   = ET.SubElement(xml_root, 'settings')
    xml_name       = ET.SubElement(xml_metadata, 'name')
    xml_brand      = ET.SubElement(xml_name, 'brand')
    xml_material   = ET.SubElement(xml_name, 'material')
    xml_color      = ET.SubElement(xml_name, 'color')
    xml_density    = ET.SubElement(xml_properties, 'density')
    xml_diameter   = ET.SubElement(xml_properties, 'diameter')
    xml_temp       = ET.SubElement(xml_settings, 'setting', key='print temperature')

    xml_brand.text    = brand
    xml_material.text = material
    xml_color.text    = color
    xml_density.text  = density
    xml_diameter.text = diameter
    xml_temp.text     = temp

    xml_raw = ET.tostring(xml_root, encoding='UTF-8')

    # Fuck this stupid API
    import xml.dom.minidom as minidom
    xml_out = minidom.parseString(xml_raw).toprettyxml(indent=' '*4, encoding='UTF-8').decode('UTF-8')

    print(filename)
    open(filename, 'w').write(xml_out)

def extract_materials(xml_filename):
    materials_data = {}

    root = ET.parse(xml_filename)
    filaments = root.find('Bloc_Filaments')
    for filament in filaments.findall('Filament'):

        name = filament.attrib['name']
        assert 'PLA' in name

        if not name.startswith('PLA'):
            continue

        brand_color = name[4:].split('-')

        if len(brand_color) > 1:
            colormap = {'rouge': 'red', 'vert': 'green', 'bleu': 'blue'}
            color = colormap[brand_color[1].lower()].title()
            color_fname = '_' + color
        else:
            color = 'Generic'
            color_fname = ''

        data = {
            'brand': brand_color[0],
            'diameter': filament.find('filament_diameter').text,
            'temp': filament.find('print_temperature').text,
            'material': 'PLA',
            'color': color,
            'density': '1.24',
        }

        material_id = '%(brand)s_%(material)s' % data
        material_id += color_fname
        material_id = material_id.replace(' ', '_').lower()

        materials_data[material_id] = data

    return materials_data

def _write_materials(xml_filename, out_dir):
    materials_data = extract_materials(xml_filename)
    for material_id, data in materials_data.items():
        filename = material_id + '.xml.fdm_material'
        filename = os.path.join(out_dir, filename)
        _write_xml(filename, **data)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: %s <xml_config.xml> <out_dir>' % sys.argv[0])
        sys.exit(0)
    _write_materials(*sys.argv[1:])
