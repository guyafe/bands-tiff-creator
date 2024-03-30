import sys
import tkinter.filedialog as fd


def create_tiff_files(dir_path):
    print('Creating tiff files in directory: ' + dir_path)
    directory_tokens = dir_path.split('_')
    print('Directory tokens: ' + str(directory_tokens))


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
