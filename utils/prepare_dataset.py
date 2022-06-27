import glob
import os
import shutil

from skimage.io import imread, imsave
import numpy as np

DEBUG = False

def prepare_data(image_source, dataset_name):
    # Prepare root directory
    dataset_root = os.path.join('datasets', dataset_name)
    try:
        os.mkdir(dataset_root)
    except FileExistsError:
        for filename in os.listdir(dataset_root):
            file_path = os.path.join(dataset_root, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    # shutil.copytree('datasets/test/labels', os.path.join(dataset_root, 'labels'))

    # Create Edges and label
    for fold in ['edges', 'list', 'labels']:
        os.mkdir(os.path.join(dataset_root, fold))

    img_list = glob.glob(os.path.join(image_source, '*'))
    tenth = len(img_list) // 10
    for i, img in enumerate(img_list):
        if not i % tenth:
            print(i // tenth * 10, '%')
        img_name = os.path.splitext(os.path.split(img)[-1])[-2]
        image = imread(img)
        imsave(
            os.path.join(dataset_root, 'edges', f'{img_name}.png'),
            np.zeros_like(image),
            check_contrast=False
        )
        if not i:
            imsave(
                os.path.join(dataset_root, 'labels', 'dummy.png'),
                np.zeros_like(image),
                check_contrast=False
            )
        if DEBUG:
            break

    print('100 %')

    # Create lists
    val_file = open(os.path.join(dataset_root, 'list', 'val.txt'), 'w')
    id_file = open(os.path.join(dataset_root, 'list', 'val_id.txt'), 'w')
    for img in img_list:
        img_file = os.path.split(img)[-1]
        img_name = os.path.splitext(img_file)[0]
        id_file.write(f'{img_name}\n')
        val_file.write(f'/images/{img_file} /labels/dummy.png\n')
        if DEBUG:
            break

    val_file.close()
    id_file.close()

    print('Run this in admin cmd: ')
    print('D: && cd', os.path.abspath(dataset_root), '&& mklink /D images', os.path.abspath(image_source))


if __name__ == '__main__':
    image_source = r'D:\Datasets\market_data\test'
    dataset_name = 'test_temp'
    prepare_data(image_source, dataset_name)
