import cv2
import numpy as np
import json
import math
from ObtenerAlturaDeCaptura import AlturaCaptura

class ROICoordinateConverter:
    def __init__(self):
        # Valores estándar para el campo de visión y resolución
        self.fov_horizontal = 69  # FoV horizontal en grados
        self.fov_vertical = 42   # FoV vertical en grados
        self.resolucion_ancho = 864 # Resolución en píxeles (ancho) 
        self.resolucion_alto = 512  # Resolución en píxeles (alto)

    def estimar_altura_de_captura(self,ply_path):
        """
        Estima la altura de captura de la nube de puntos PLY.
        """
        altura_captura = AlturaCaptura(ply_path)
        return altura_captura.calcular_altura()
    
    def calcular_escala(self, altura_captura):
        """
        Calcula las escalas de conversión de píxeles a metros basadas en la altura de captura.
        """
        ancho_real = 2 * altura_captura * math.tan(math.radians(self.fov_horizontal / 2))
        alto_real = 2 * altura_captura * math.tan(math.radians(self.fov_vertical / 2))
        escala_horizontal = ancho_real / self.resolucion_ancho
        escala_vertical = alto_real / self.resolucion_alto
        return escala_horizontal, escala_vertical

    def convertir_pixeles_a_metros(self, x1_pix, y1_pix, x2_pix, y2_pix, escala_horizontal, escala_vertical, centro_x, centro_y):
        """
        Convierte coordenadas de píxeles a metros.
        """
        x1_metros = (x2_pix - centro_x) * escala_horizontal
        y1_metros = (y2_pix - centro_y ) * escala_vertical
        x2_metros = (x1_pix - centro_x ) * escala_horizontal
        y2_metros = (y1_pix - centro_y) * escala_vertical
        return x1_metros, y1_metros, x2_metros, y2_metros

    def definir_roi_y_guardar(self, alturaDeCaptura, image_path, output_path_base, txt_path):
        """
        Define la ROI en la imagen y guarda las coordenadas en metros en un archivo TXT con formato JSON.
        """
        # Cargar imagen
        depth_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        altura, anchura = depth_image.shape[:2]
        centro_x, centro_y = anchura // 2, altura // 2

        # Leer las coordenadas desde el archivo TXT y procesar cada línea
        with open(txt_path, 'r') as file:
            lines = file.readlines()

        for index, coords in enumerate(lines):
            x1, y1, x2, y2 = [int(float(coord)) for coord in coords.strip()[1:-1].split(', ')]
            
            # Calcular escala según la altura de captura
            escala_horizontal, escala_vertical = self.calcular_escala(alturaDeCaptura)
            
            # Convertir coordenadas de píxeles a metros
            x1_metros, y1_metros, x2_metros, y2_metros = self.convertir_pixeles_a_metros(
                x1, y1, x2, y2, escala_horizontal, escala_vertical, centro_x, centro_y)

            # Dibujar el rectángulo de la ROI en la imagen
            cv2.rectangle(depth_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Guardar las coordenadas de la ROI en un archivo TXT con formato JSON en otra carpeta de coordenadas transformadas
            
            roi_data = {'x1': x1_metros, 'y1': y1_metros, 'x2': x2_metros, 'y2': y2_metros}
            output_file = f"{output_path_base}_{index}.txt"  # Construye el nombre del archivo con índice
            with open(output_file, 'w') as file:
                json.dump(roi_data, file)

        # Mostrar la imagen con todas las ROIs dibujadas
        cv2.imshow("ROI en Imagen de Profundidad", depth_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def convertir_radio_pixeles_a_metros(self, radio_pixeles, escala_horizontal):
        """
        Convierte el radio del círculo de píxeles a metros usando la escala horizontal.
        """
        radio_metros = radio_pixeles * escala_horizontal
        return radio_metros
    
    #funcion para el manejo de la transformacion de las coordenadas de la ROI a metros dentro de la misma clase para el caso de convertir el radio del circulo a metros
    def manejo_transformacion_roi(self, radio, image_path, centrodelCirculo, altura_captura):
        """
        Maneja la transformación de las coordenadas de la ROI a metros.
        """
        imagen_original = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        altura, anchura = imagen_original.shape[:2]
        centro_x, centro_y = anchura // 2, altura // 2
        
        calcular_escala = self.calcular_escala(altura_captura)

        #Convertir radio del círculo a metros
        radio_metros = self.convertir_radio_pixeles_a_metros(radio, calcular_escala[0])

        return radio_metros