import os
import cv2
import numpy as np

def draw_labels(img, labels, colors, class_names):
    for label in labels:
        color = colors[label[0]]
        x, y, w, h = label[1:]
        xmin, ymin, xmax, ymax = map(int, [x * img.shape[1] - w * img.shape[1] / 2,
                                   y * img.shape[0] - h * img.shape[0] / 2,
                                   x * img.shape[1] + w * img.shape[1] / 2,
                                   y * img.shape[0] + h * img.shape[0] / 2])
        print('xmin:', xmin, 'ymin:', ymin, 'xmax:', xmax, 'ymax:', ymax)  # exibir coordenadas para depuração
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 2)
        cv2.putText(img, class_names[label[0]], (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        print('label:', class_names[label[0]], 'x:', x, 'y:', y, 'w:', w, 'h:', h)  # exibir coordenadas para depuração


def visualize(image_path, label_path, class_names):
    colors = np.random.uniform(0, 255, size=(len(class_names), 3))
    labels = []
    with open(label_path, 'r') as f:
        for line in f:
            label = line.strip().split()
            label = [int(label[0])] + [float(x) for x in label[1:]]
            labels.append(label)
    img = cv2.imread(image_path)
    draw_labels(img, labels, colors, class_names)
    cv2.imshow('Image', img)
    cv2.waitKey(0)

def visualize_folder(image_folder, label_folder, class_names):
    image_files = os.listdir(image_folder)
    for image_file in image_files:
        # Filtra apenas os arquivos com extensão .jpg ou .png
        if not image_file.endswith('.jpg') and not image_file.endswith('.png'):
            continue
        image_path = os.path.join(image_folder, image_file)
        label_path = os.path.join(label_folder, os.path.splitext(image_file)[0] + '.txt')
        if not os.path.exists(label_path):
            continue
        visualize(image_path, label_path, class_names)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    class_names_file = 'classes.names'
    with open(class_names_file, 'r') as f:
        class_names = [line.strip() for line in f.readlines()]
    image_folder = 'images'
    label_folder = 'labels/yolo'
    visualize_folder(image_folder, label_folder, class_names)

