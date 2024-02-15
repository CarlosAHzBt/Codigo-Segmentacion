from DetectorDeBaches import DetectorDeBaches
from ManejadorDeMascaraDeSegmentacion import ManejadorDeMascaraSegmentacion
from ManejadorDeBag.ProcesadorBags import ProcesadorBags
from AdministradorDeCarpetas import AdministradorDeCarpetas
from ManejadorDeImagenes    import ManejadorDeImagenes
from CargadorDeRecursos import CargadorDeRecursos
from TransformacionROI import ROICoordinateConverter
import os


class Main:
    def __init__(self):
        self.modelo = CargadorDeRecursos("ModeloDeSegmentacion/model_state_dict.pth")
        self.administrador_de_carpetas = AdministradorDeCarpetas()
    def cargar_modelo(self):
        modelo = self.modelo.cargar_modelo()
        return modelo
        
    def segmentar_imagenes(self, carpeta_base):
        print("Empezando a segmentar imágenes...")
        modelo = self.cargar_modelo()
        manejador_de_imagenes = ManejadorDeImagenes()

            # Recorre las carpetas de imágenes dentro de la carpeta base.
        for carpeta_imagen in self.administrador_de_carpetas.listar_carpetas_de_imagenes(carpeta_base):
            partes_ruta = carpeta_imagen.split(os.sep)
            # Asumiendo que la estructura de carpetas es ProcesamientoDeBags/BacheRef2/Imagenes
            nombre_bag = partes_ruta[-2] if len(partes_ruta) > 2 else 'DefaultBagName'
            ruta_carpeta_segmentadas = os.path.join(carpeta_base, nombre_bag, "imagenes_segmentadas")
            ruta_bag = os.path.join(carpeta_base, nombre_bag)
            


            # Crea la carpeta de imágenes segmentadas si no existe.
            self.administrador_de_carpetas.crear_carpeta_si_no_existe(ruta_carpeta_segmentadas)

            # Itera sobre las imágenes en la carpeta actual del bag.
            for imagen_path in self.administrador_de_carpetas.iterar_sobre_carpetas_de_imagenes(carpeta_imagen):
                segmentador = ManejadorDeMascaraSegmentacion()
                try:
                    imagen_segmentada = segmentador.aplicar_segmentacion(modelo, imagen_path)
                    #Reescalar la imagen segmentada al tamaño original
                    imagen_segmentada = segmentador.redimensionar_mascara(imagen_segmentada)
                    #Etiquetar y obtener las coordenadas de la imagen segmentada
                    regiones = segmentador.etiquetar_region_mascaraSegmentacion(imagen_segmentada)
                    #Filtrar las regiones de la imagen segmentada por tamaño
                    regiones_filtradas = segmentador.filtrar_regiones_de_segmentacion_por_tamaño(regiones, 1000)
                    #Guardar las coordenadas de las regiones filtradas
                    segmentador.guardar_coordenadas(ruta_bag, os.path.basename(imagen_path), regiones_filtradas)
                    # Construye la ruta completa del archivo donde se guardará la imagen segmentada.
                    nombre_archivo_segmentado = f"segmentada_{os.path.basename(imagen_path)}"
                    ruta_completa_archivo = os.path.join(ruta_carpeta_segmentadas, nombre_archivo_segmentado)
                    
                    # Suponiendo que imagen_path es la ruta a la imagen original como 'ProcesamientoDeBags/BacheRef2/Imagenes/frame_00000.png'
                    nombre_base_imagen = os.path.basename(imagen_path)  # Esto dará 'frame_00000.png'
                    nombre_archivo_coordenadas = f"{nombre_base_imagen}_1.txt"  # Esto dará 'frame_00000.png_1.txt'
                    
                    ruta_directorio_coordenadas = os.path.join(ruta_bag, "coordenadas")
                    # Ahora construye la ruta completa al archivo de coordenadas
                    ruta_coordenadas = os.path.join(ruta_directorio_coordenadas, nombre_archivo_coordenadas)
                    
                    # Construye las rutas necesarias para procesar contornos y círculo
                    #nombre_archivo_coordenadas = os.path.splitext(os.path.basename(imagen_path)) + ".txt"
                    coordenadas_path = os.path.join(ruta_bag, "coordenadas", nombre_archivo_coordenadas)
                    ruta_salida = os.path.join(ruta_carpeta_segmentadas, f"final_{os.path.basename(imagen_path)}")
                    segmentador.procesar_imagen(imagen_path, ruta_coordenadas, ruta_salida)


                    # Guarda la imagen segmentada utilizando el manejador de imágenes.
                    manejador_de_imagenes.guardar_imagen_segmentada(imagen_segmentada, ruta_completa_archivo)
                    

                    #Medir el circulo del bache para ver si es un bache o no un bache debe ser mayor a 15cm de diametro
                    try:
                        #Generar la ruta a la carpeta de ply
                        ruta_ply = os.path.join(ruta_bag, "ply")
                        ply_path = os.path.join(ruta_ply, f"{os.path.splitext(os.path.basename(imagen_path))[0]}.ply")
                        if not os.path.isfile(ply_path):
                            raise FileNotFoundError(f"No se encontró el archivo ply: {ply_path}")

                        #Cargar la nube de puntos para obtener la escala de conversion de pixeles a metros
                        nube_de_puntos = self.modelo.cargar_ply(ply_path)
                        #Obtener el circulo inscrito
                        circulo_inscrito = segmentador.dibujar_circulo_inscrito(nube_de_puntos, coordenadas_path)
                        #obtener escala de conversion de pixeles a metros obteniedno la altura de captura
                        altura_captura = ROICoordinateConverter
                        superficie_estimada = altura_captura.estimar_altura_de_captura(nube_de_puntos)
                        print(altura_captura.manejo_transformacion_roi(circulo_inscrito, imagen_path, superficie_estimada))
                    except Exception as e:
                        print(f"Error al medir el circulo inscrito: {e}")

                        


                        
                        
                        nube_de_puntos = self.modelo.cargar_ply(os.path.join(ruta_bag, "nube_de_puntos.ply"))
                except Exception as e:
                    print(f"Error al segmentar la imagen {imagen_path}: {e}")
                


    def extraer_datos_de_bagFiles(self, carpeta_bags):
        print("Extrayendo datos de los bag files")
        procesador = ProcesadorBags(carpeta_bags)
        procesador.process_bag_files()
        print("Datos extraidos de los bag files")
    def proceso(self):
        self.extraer_datos_de_bagFiles(carpeta_bags)
        carpeta="ProcesamientoDeBags"
        self.segmentar_imagenes(carpeta)


if __name__ == "__main__":
    carpeta_bags = "bag"
    app_principal = Main()
    app_principal.proceso()