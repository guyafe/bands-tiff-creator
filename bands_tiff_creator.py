import os
import sys
import tkinter.filedialog as fd

from jp2_file import Jp2File
from resolution_dir import ResolutionDir

DATE_INDEX_IN_SPLITTED_SENTINEL_DIRECTORY_TOKENS = 2
RELATIVE_PATH_TO_GRANULE_DIR = 'GRANULE'
RELATIVE_PATH_TO_IMG_DATA_DIRS = 'IMG_DATA'
RESOLUTION_DIR_PREFIX = 'R'
L2A_DIR_PREFIX = 'L2A'
JP2_FILE_EXTENSION = '.jp2'
JP2_FILE_NUMBER_OF_SPLITTED_TOKENS = 4
JP2_FILE_BAND_TOKEN_INDEX = 2
BAND_PREFIX = 'B'


def get_resolutions_dirs(dir_path):
    granule_dir = os.path.join(dir_path, RELATIVE_PATH_TO_GRANULE_DIR)
    l2a_dirs = [l2a for l2a in os.listdir(granule_dir) if l2a.startswith(L2A_DIR_PREFIX)]
    if len(l2a_dirs) != 1:
        print(f'Expected 1 granule directory, but found {len(l2a_dirs)}')
        exit(1)
    l2a_dir = os.path.join(granule_dir, l2a_dirs[0])
    image_data_dir = os.path.join(l2a_dir, RELATIVE_PATH_TO_IMG_DATA_DIRS)
    print(f'Image data dir: {image_data_dir}')
    resolution_dirs = [ResolutionDir(name, os.path.join(image_data_dir, name)) for name in
                       os.listdir(image_data_dir) if name.startswith(RESOLUTION_DIR_PREFIX)]
    print(f'Found {len(resolution_dirs)} resolution directories')
    return resolution_dirs


def parse_band_number(band):
    return int(''.join(c for c in band if c.isdigit()))


def create_band_files(resolutions_dir):
    jp2_file_names = [jp2_file_name for jp2_file_name in os.listdir(resolutions_dir.path) if
                      jp2_file_name.endswith(JP2_FILE_EXTENSION)]
    jp2_band_files = []
    for jp2_file_name in jp2_file_names:
        jp2_file_tokens = jp2_file_name.split('_')
        if len(jp2_file_tokens) == JP2_FILE_NUMBER_OF_SPLITTED_TOKENS and jp2_file_tokens[
            JP2_FILE_BAND_TOKEN_INDEX].startswith(BAND_PREFIX):
            band = jp2_file_tokens[JP2_FILE_BAND_TOKEN_INDEX]
            jp2_band_files.append(Jp2File(jp2_file_name, band, os.path.join(resolutions_dir.path, jp2_file_name)))
    jp2_band_files.sort(key=lambda jp2_file: parse_band_number(jp2_file.band))
    return jp2_band_files


def create_tiff_files_for_resolution(resolutions_dir, date):
    print(f'Creating tiff files for resolution: {resolutions_dir.name}')
    tiff_file_name = f'sentinel_{resolutions_dir.name}_{date}.tiff'
    print(f'Tiff file name: {tiff_file_name}')
    jp2_band_files = create_band_files(resolutions_dir)
    print(f'Found {len(jp2_band_files)} band files')


def create_tiff_files(dir_path):
    directory_tokens = dir_path.split('_')
    date = directory_tokens[DATE_INDEX_IN_SPLITTED_SENTINEL_DIRECTORY_TOKENS]
    print(f'Creating tiff files for date: {date} in directory: {dir_path}')
    resolutions_dirs = get_resolutions_dirs(dir_path)
    for resolutions_dir in resolutions_dirs:
        create_tiff_files_for_resolution(resolutions_dir, date)


def main():
    print('Starting band tiff creator...')
    if len(sys.argv) == 2:
        initial_dir_path = sys.argv[1]
        dir_path = fd.askdirectory(initialdir=initial_dir_path)
    else:
        dir_path = fd.askdirectory()

    create_tiff_files(dir_path)


if __name__ == '__main__':
    main()
