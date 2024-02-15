import os

class AdministradorDeCarpetas:
    @staticmethod
    def listar_archivos(carpeta):
        for subdir, dirs, files in os.walk(carpeta):
            for file in files:
                yield os.path.join(subdir, file)

    @staticmethod
    def crear_carpeta_si_no_existe(ruta):
        if not os.path.exists(ruta):
            os.makedirs(ruta)

    def buscar_archivos_en_subcarpetas(self, carpeta, extensiones):
        archivos = []
        for archivo in self.listar_archivos(carpeta):
            if archivo.endswith(extensiones):
                archivos.append(archivo)
        return archivos

    def iterar_sobre_carpetas(self, carpeta):
        for subdir, dirs, files in os.walk(carpeta):
            yield subdir 
    
    #Crear lista de las carpetas de imagenes
    def listar_carpetas_de_imagenes(self, carpeta):
        carpetas = []
        for subdir, dirs, files in os.walk(carpeta):
            # Solo agregar las carpetas que contienen imágenes
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg')):
                    carpetas.append(subdir)
                    break
        return carpetas
    #Iterar sobre la lista de carpetas e iterar las imagenes que estan en la carpeta
    def iterar_sobre_carpetas_de_imagenes(self, carpeta):
        for subdir, dirs, files in os.walk(carpeta):
            for file in files:
                yield os.path.join(subdir, file)
                
    #Crear carpeta en el directorio actual
    def crear_carpeta_en_bag_actual(self,bag_actual, nombre_carpeta):
        ruta_carpeta = os.path.join(bag_actual, nombre_carpeta)
        self.crear_carpeta_si_no_existe(ruta_carpeta)
        return ruta_carpeta
        
