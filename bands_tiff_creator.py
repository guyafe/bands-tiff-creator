import os
import sys
import tkinter.filedialog as fd

from resolution_dir import ResolutionDir

DATE_INDEX_IN_SPLITTED_SENTINEL_DIRECTORY_TOKENS = 2
RELATIVE_PATH_TO_GRANULE_DIR = 'GRANULE'
RELATIVE_PATH_TO_IMG_DATA_DIRS = 'IMG_DATA'
RESOLUTION_DIR_PREFIX = 'R'
L2A_DIR_PREFIX = 'L2A'


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


def create_tiff_files_for_resolution(resolutions_dir, date):
    print(f'Creating tiff files for resolution: {resolutions_dir.name}')
    tiff_file_name = f'sentinel_{resolutions_dir.name}_{date}.tiff'
    print(f'Tiff file name: {tiff_file_name}')


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
