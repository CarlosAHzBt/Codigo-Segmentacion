#Clase encargada de dar procesamiento a las imagenes
from PIL import Image
from torchvision.transforms import Compose, ToTensor, Normalize
import numpy as np
import os
import matplotlib.pyplot as plt


class ManejadorDeImagenes:
    def __init__(self):
        pass

    def cargar_imagen(self, ruta_imagen):
        imagen = Image.open(ruta_imagen)
        return imagen

    def guardar_imagen(self, imagen, nombre, ruta):
        imagen.save(os.path.join(ruta, nombre))

    def prepara_imagen_segmentacion(self, imagen, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]):
        """Convierte la imagen en una matriz Numpy y le aplica un filtro de mediana"""
        imagen = Image.open(imagen).convert("RGB")
        transformaciones = Compose([
            ToTensor(),
            Normalize(mean, std),
        ])
        return transformaciones(imagen).unsqueeze(0)
    
    def guardar_imagen_segmentada(self, imagen_segmentada, ruta_carpeta_segmentadas):
        # Construye la ruta completa del archivo donde se guardará la imagen segmentada
        ruta_completa_archivo = os.path.join(ruta_carpeta_segmentadas)

        # Guarda la imagen segmentada utilizando Matplotlib
        plt.imsave(ruta_completa_archivo, imagen_segmentada, cmap='viridis')
