from DetectorDeBaches import DetectorDeBaches
from skimage.transform import resize
from skimage.measure import label, regionprops  # Importar la funcion label
import os
import cv2 as cv
import numpy as np

class ManejadorDeMascaraSegmentacion:
    def __init__(self):
        pass

    def redimensionar_mascara(self, imagen):
        #mascara_redimensionada = DetectorDeBaches.detectar(imagen)
        mascara_redimensionada = resize(imagen, (480, 848), order=0, preserve_range=True, anti_aliasing=False).astype(int)
        return mascara_redimensionada

        
    def etiquetar_region_mascaraSegmentacion(self,imagen):
        #mascara_redimensioanda = self.redimensionar_mascara(imagen)
        labeled_baches_resized = label(imagen, connectivity=2)
        regions_resized = regionprops(labeled_baches_resized)
        return regions_resized
    
    def filtrar_regiones_de_segmentacion_por_tamaño(self,imagen, area_minima):
        region_filtrada = [region for region in imagen if region.area >= area_minima]

        return region_filtrada
    
    def guardar_coordenadas(self, nombre_bag, nombre_frame, regiones):
        # Ruta al directorio del bag específico
        ruta_bag = os.path.join(nombre_bag)
        
        # Ruta a la carpeta de coordenadas dentro del directorio del bag
        ruta_coordenadas = os.path.join(ruta_bag, 'coordenadas')
        
        # Crear la carpeta de coordenadas si no existe
        os.makedirs(ruta_coordenadas, exist_ok=True)
        
        # Por cada región detectada, guardar un archivo de texto con las coordenadas
        for i, region in enumerate(regiones, start=1):
            nombre_archivo = f"{nombre_frame}_{i}.txt"
            ruta_archivo = os.path.join(ruta_coordenadas, nombre_archivo)
            
            with open(ruta_archivo, "w") as file:
                for y, x in region.coords:
                    file.write(f"{x},{y}\n")


    def crear_contornos(self, imagen_segmentada, coordenadas_path):
        # Cargar la imagen segmentada
        imagen = cv.imread(imagen_segmentada)

        # Cargar las coordenadas que incluyen el contorno y el interior del bache
        coordenadas = np.loadtxt(coordenadas_path, delimiter=',')

        # Crear una imagen en negro con las mismas dimensiones que la imagen segmentada
        imagen_contorno = np.zeros(imagen.shape, dtype=np.uint8)

        # Colorear los puntos especificados en el archivo txt
        for x, y in coordenadas.astype(np.int32):
            imagen_contorno[y, x] = [255, 255, 255]

        # Encontrar los contornos en la imagen de puntos
        contornos, _ = cv.findContours(cv.cvtColor(imagen_contorno, cv.COLOR_BGR2GRAY), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Dibujar el contorno más grande
        contorno_externo = max(contornos, key=cv.contourArea)
        cv.drawContours(imagen, [contorno_externo], -1, (0, 255, 0), 2)

        return imagen, contorno_externo


    def dibujar_circulo_inscrito(self, imagen, contorno_externo):
        # Buscar el radio máximo y el centro del círculo
        radio_maximo = 0
        centro_circulo = (0, 0)

        # Itera sobre los puntos del contorno
        for punto in np.argwhere(cv.cvtColor(imagen, cv.COLOR_BGR2GRAY)):
            dist = cv.pointPolygonTest(contorno_externo, (int(punto[1]), int(punto[0])), True)
            if dist > radio_maximo:
                radio_maximo = dist
                centro_circulo = (int(punto[1]), int(punto[0]))

        # Dibujar el círculo máximo inscrito en la imagen
        cv.circle(imagen, centro_circulo, int(radio_maximo), (0, 255, 0), 2)

        return imagen

    def procesar_imagen(self, imagen_segmentada, coordenadas_path, ruta_salida):
        imagen, contorno_externo = self.crear_contornos(imagen_segmentada, coordenadas_path)
        imagen_con_circulo = self.dibujar_circulo_inscrito(imagen, contorno_externo)

        # Guardar la imagen final
        #cv.imwrite(ruta_salida, imagen_con_circulo)
    def aplicar_segmentacion(self,modelo,imagen_a_segmentar):
        segmentar = DetectorDeBaches(modelo)
        mascara_segmenteada = segmentar.detectar(imagen_a_segmentar)
        return mascara_segmenteada