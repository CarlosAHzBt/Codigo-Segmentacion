import torch
from PIL import Image
from torchvision.transforms import Compose, ToTensor, Normalize
from CargarModelo import CargarModelo

class CargadorDeRecursos:
    def __init__(self,modelo):
        self.modelo = modelo
    
    def cargar_modelo(self):
        Objetomodelo = CargarModelo()
        modelo = Objetomodelo.cargar_modelo(self.modelo)
        modelo.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        return modelo

    @staticmethod
    def cargar_imagen(path_imagen, mean, std):
        imagen = Image.open(path_imagen).convert("RGB")
        transformaciones = Compose([
            ToTensor(),
            Normalize(mean=mean, std=std),
        ])
        return transformaciones(imagen).unsqueeze(0)
    