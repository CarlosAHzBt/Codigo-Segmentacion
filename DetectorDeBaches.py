import torch
from PIL import Image
from torchvision.transforms import Compose, ToTensor, Normalize
from CargarModelo import CargarModelo
from CargadorDeRecursos import CargadorDeRecursos
from ManejadorDeImagenes import ManejadorDeImagenes
import numpy as np

class DetectorDeBaches:
    def __init__(self, modelo):
        self.imagen_a_segmentar = ManejadorDeImagenes()
        self.modelo = modelo


    def detectar(self, imagen):
        pixel_values = self.imagen_a_segmentar.prepara_imagen_segmentacion(imagen)
        with torch.no_grad():
            predicciones = self.modelo(pixel_values)
            #predicciones = self.modelo(pixel_values=pixel_values)
            predicted_mask = predicciones[0].argmax(dim=1).squeeze().cpu().numpy()
        return predicted_mask