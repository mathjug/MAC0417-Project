import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

def show_samples_all_classes(images_folder, n_samples_per_class = 7):
  dict_images = store_images_dictionary(images_folder)
  plt.rcParams['figure.figsize'] = (10.0, 8.0)
  n_classes = len(dict_images)
  for index, (item_label, image_paths) in enumerate(dict_images.items()):
    random_image_paths = np.random.choice(image_paths, size=n_samples_per_class, replace=False)
    for i in range(n_samples_per_class):
        image_path = random_image_paths[i]
        image = mpimg.imread(image_path)
        plt_idx = i * n_classes + index + 1  # calculate plot location in the grid
        plt.subplot(n_samples_per_class, n_classes, plt_idx)
        plt.imshow(image)
        plt.axis('off')
        if i == 0:
            plt.title(item_label)
  plt.show()

def show_class(label, images_folder, n_samples = 20):
  lower_label = label.lower()
  dict_images = store_images_dictionary(images_folder)
  plt.rcParams['figure.figsize'] = (10.0, 8.0)
  for i in range(n_samples):
      image_path = dict_images[lower_label][i]
      image = mpimg.imread(image_path)
      plt_idx = 4 * (i // 4) + (i % 4) + 1  # calculate plot location in the grid
      plt.subplot(4, 5, plt_idx)
      plt.imshow(image)
      plt.axis('off')
  plt.suptitle(label, fontsize=24, y=0.95)
  plt.show()

def show_global_table(images_folder):
  print("================================================================")
  print("Tabela Global Sumária:")
  classes = list_classes(images_folder)
  print("--> Nome das Classes:", classes)
  print("--> Número de Classes:", len(classes))
  n_images, total_size = count_images_and_size(images_folder)
  print("--> Número de Imagens:", n_images)
  print("--> Tamanho da Base (Bytes): ", total_size, " (", "{:.2f}".format(total_size / 1e6), " MB)", sep="")
  height, width = get_resolution(images_folder)
  print("--> Resolução das Imagens:", height, "linhas por", width, "colunas")
  print("================================================================")

def show_class_tables(images_folder):
    dict_images = store_images_dictionary(images_folder)
    csv_path = os.path.join(images_folder, "metadata.csv")
    df = pd.read_csv(csv_path)

    for item_class in dict_images.keys():
        mask = (df['Item_1'] == item_class) | (df['Item_2'] == item_class) | (df['Item_3'] == item_class)
        filtered_data = df.loc[mask]
        print("\n================================================================")
        light_variations = filtered_data[['Local', 'Periodo']].drop_duplicates().values
        back_variations = filtered_data[["Fundo"]].drop_duplicates().values
        n_items = filtered_data[["N_Itens"]].drop_duplicates().values
        n_images = len(dict_images[item_class])
        print(" ==> Nome da classe:", item_class)
        print(" ==> Numero de objetos por imagem:", n_items[0][0])
        print(" ==> Variacoes de fundo:", back_variations.shape[0], end=" -> ")
        for back in back_variations:
            print(back[0], end=" ")
        print()
        print(" ==> Variacoes de iluminacao:", light_variations.shape[0], end=" -> ")
        for light in light_variations:
            print(tuple(light), end=" ")
        print()
        print(" ==> Total de amostras:", n_images)
        print("================================================================")

################# SET OF AUXILIARY METHODS ###################

def store_images_dictionary(images_folder):
    csv_filename = "metadata.csv"
    csv_path = os.path.join(images_folder, csv_filename)
    data = pd.read_csv(csv_path)
    item_to_images = {}
    for index, row in data.iterrows():
        image_file = row['Nome_da_Imagem']
        image_path = os.path.join(images_folder, image_file)
        items = [row['Item_1'], row['Item_2'], row['Item_3']]
        for item in items:
            if item not in item_to_images:
                item_to_images[item] = []
            item_to_images[item].append(image_path)
    return item_to_images

def list_classes(images_folder):
    dict_images = store_images_dictionary(images_folder)
    return list(dict_images.keys())

def count_images_and_size(images_folder):
    csv_path = os.path.join(images_folder, "metadata.csv")
    df = pd.read_csv(csv_path)
    num_images = len(df)
    total_size = df['Image_Size'].sum()
    return num_images, total_size

def get_resolution(images_folder):
  csv_path = os.path.join(images_folder, "metadata.csv")
  df = pd.read_csv(csv_path)
  height = df['Rows'][0]
  width = df['Columns'][0]
  return height, width