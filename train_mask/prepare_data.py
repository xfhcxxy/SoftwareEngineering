import os
import cv2

"""
数据下载地址https://www.kaggle.com/prasoonkottarathil/face-mask-lite-dataset
"""
original_dataset_dir = 'F:/data/face_mask'
original_dataset_with_mask_dir = os.path.join(original_dataset_dir, 'with_mask')
original_dataset_without_mask_dir = os.path.join(original_dataset_dir, 'without_mask')

base_dir = 'data'
base_train_dir = os.path.join(base_dir, 'train')
base_test_dir = os.path.join(base_dir, 'test')
base_validation_dir = os.path.join(base_dir, 'validation')
base_train_with_mask_dir = os.path.join(base_train_dir, 'with_mask')
base_train_without_mask_dir = os.path.join(base_train_dir, 'without_mask')
base_test_with_mask_dir = os.path.join(base_test_dir, 'with_mask')
base_test_without_mask_dir = os.path.join(base_test_dir, 'without_mask')
base_validation_with_mask_dir = os.path.join(base_validation_dir, 'with_mask')
base_validation_without_mask_dir = os.path.join(base_validation_dir, 'without_mask')


names = os.listdir(original_dataset_with_mask_dir)
#names = names[:1000]
num = len(names)

num_train = int(num * 0.7)
num_test = int(num * 0.15)
num_validation = num - num_train - num_test

names_train = names[0:num_train]
names_test = names[num_train:num_train+num_test]
names_validation = names[num_train+num_test:]


for name in names_train:
    print(name)
    image = cv2.imread(original_dataset_with_mask_dir+'/'+name)
    image2 = cv2.resize(image, (150, 150))
    cv2.imwrite(base_train_with_mask_dir+'/'+name, image2)


for name in names_test:
    print(name)
    image = cv2.imread(original_dataset_with_mask_dir + '/' + name)
    image2 = cv2.resize(image, (150, 150))
    cv2.imwrite(base_test_with_mask_dir + '/' + name, image2)

for name in names_validation:
    print(name)
    image = cv2.imread(original_dataset_with_mask_dir + '/' + name)
    image2 = cv2.resize(image, (150, 150))
    cv2.imwrite(base_validation_with_mask_dir + '/' + name, image2)

names = os.listdir(original_dataset_without_mask_dir)
#names = names[:1000]
num = len(names)

num_train = int(num * 0.7)
num_test = int(num * 0.15)
num_validation = num - num_train - num_test

names_train = names[0:num_train]
names_test = names[num_train:num_train + num_test]
names_validation = names[num_train + num_test:]

for name in names_train:
    print(name)
    image = cv2.imread(original_dataset_without_mask_dir + '/' + name)
    image2 = cv2.resize(image, (150, 150))
    cv2.imwrite(base_train_without_mask_dir + '/' + name, image2)

for name in names_test:
    print(name)
    image = cv2.imread(original_dataset_without_mask_dir + '/' + name)
    image2 = cv2.resize(image, (150, 150))
    cv2.imwrite(base_test_without_mask_dir + '/' + name, image2)

for name in names_validation:
    print(name)
    image = cv2.imread(original_dataset_without_mask_dir + '/' + name)
    image2 = cv2.resize(image, (150, 150))
    cv2.imwrite(base_validation_without_mask_dir + '/' + name, image2)
