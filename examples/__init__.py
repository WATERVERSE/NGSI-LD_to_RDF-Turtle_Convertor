import pathlib
from os.path import join

parent_path = pathlib.Path(__file__).parent.absolute()

file_json_ld = 'sample_UK_rain.json'
file_path_json_ld = join(parent_path, file_json_ld)

ttl_file_name = 'sample_UK_rain.ttl'
destination_of_converted_file = join(parent_path, ttl_file_name)

ttl_viz_name = 'visualization knmi 2510.png'
destination_png = join(parent_path, ttl_viz_name)
