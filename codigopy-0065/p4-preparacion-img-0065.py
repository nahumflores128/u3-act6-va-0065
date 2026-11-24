import cv2
import numpy as np
import os
import csv

# ==========================================
# DATOS DEL ALUMNO
# Nombre: [Tu Nombre Completo]
# Número de Control: [Tu Número de Control] (Terminación 0065)
# ==========================================

# 1. Configuración inicial
carpeta_original = "img-original-0065"
carpeta_preparadas = "img-preparadas-0065"
carpeta_resultados = "resultados-img-0065"

ANCHO_DESTINO = 224
ALTO_DESTINO = 224

# Crear carpetas de salida si no existen
os.makedirs(carpeta_preparadas, exist_ok=True)
os.makedirs(carpeta_resultados, exist_ok=True)

categorias = ["Zanahoria", "Rabanos"]
reporte = []
imagenes_procesadas = 0
imagenes_aprobadas = 0

print("🚀 Iniciando preparación de imágenes PNG (Zanahoria y Rabanos)...\n")

# 2. Recorrer cada categoría y sus archivos específicos (1 al 5)
for categoria in categorias:
    ruta_origen = os.path.join(carpeta_original, categoria)
    ruta_destino = os.path.join(carpeta_preparadas, categoria)
    
    os.makedirs(ruta_destino, exist_ok=True)
    
    if not os.path.exists(ruta_origen):
        print(f"⚠️ La carpeta {ruta_origen} no existe. Saltando...")
        continue

    prefijo = "Zanahoria" if categoria == "Zanahoria" else "Rabano"
    nombres_esperados = [f"{prefijo}{i}.png" for i in range(1, 6)]

    for nombre_archivo in nombres_esperados:
        ruta_imagen = os.path.join(ruta_origen, nombre_archivo)
        
        if not os.path.isfile(ruta_imagen):
            print(f"⚠️ No se encontró la imagen: {nombre_archivo} en {ruta_origen}")
            reporte.append([categoria, nombre_archivo, "NO ENCONTRADO", "-", "-", "-", "-", "-", "-", "REVISAR"])
            continue
            
        print(f"📸 Procesando: {nombre_archivo}")
        
        # 3. Leer la imagen PNG
        imagen = cv2.imread(ruta_imagen)
        if imagen is None:
            print(f"   ❌ Error: No se pudo leer la imagen.")
            reporte.append([categoria, nombre_archivo, "ERROR", "-", "-", "-", "-", "-", "-", "REVISAR"])
            continue
            
        imagenes_procesadas += 1
        alto_orig, ancho_orig, canales = imagen.shape
        print(f"   📏 Dimensiones originales: {ancho_orig} x {alto_orig}")
        
        # 4. Redimensionar la imagen
        imagen_redimensionada = cv2.resize(imagen, (ANCHO_DESTINO, ALTO_DESTINO), interpolation=cv2.INTER_AREA)
        print(f"   📐 Dimensiones nuevas: {ANCHO_DESTINO} x {ALTO_DESTINO}")
        
        # Guardar ÚNICAMENTE la imagen redimensionada en formato PNG
        ruta_png = os.path.join(ruta_destino, nombre_archivo)
        cv2.imwrite(ruta_png, imagen_redimensionada)
        
        # 5. Calcular normalización para el reporte CSV
        imagen_normalizada = imagen_redimensionada.astype(np.float32) / 255.0
        val_min = float(np.min(imagen_normalizada))
        val_max = float(np.max(imagen_normalizada))
        print(f"   🔢 Rango normalizado: {val_min:.3f} a {val_max:.3f}")
        
        # 6. Evaluar automáticamente el resultado
        dimensiones_correctas = (imagen_redimensionada.shape[0] == ALTO_DESTINO and 
                                 imagen_redimensionada.shape[1] == ANCHO_DESTINO)
        rango_correcto = (val_min >= 0.0 and val_max <= 1.0)
        archivo_guardado = os.path.isfile(ruta_png)
        
        if dimensiones_correctas and rango_correcto and archivo_guardado:
            estado = "APROBADA"
            imagenes_aprobadas += 1
            print(f"   ✅ Evaluación: APROBADA\n")
        else:
            estado = "REVISAR"
            print(f"   ⚠️ Evaluación: REVISAR\n")
            
        # 7. Guardar datos en la lista para el reporte final
        reporte.append([
            categoria, nombre_archivo, "OK", ancho_orig, alto_orig,
            ANCHO_DESTINO, ALTO_DESTINO, round(val_min, 3), round(val_max, 3), estado
        ])

# 8. Generar el reporte en formato CSV
ruta_reporte = os.path.join(carpeta_resultados, "reporte_preparacion_0065.csv")
with open(ruta_reporte, "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["Nombre:", "[Tu Nombre Completo]", "NC:", "[Tu Número de Control]"])
    escritor.writerow([])
    escritor.writerow([
        "Categoría", "Archivo original", "Lectura", 
        "Ancho original", "Alto original", "Ancho preparado", "Alto preparado", 
        "Valor mínimo norm.", "Valor máximo norm.", "Evaluación"
    ])
    escritor.writerows(reporte)

# 9. Resumen final en consola
print("=" * 45)
print("🎉 RESUMEN DE LA PRÁCTICA")
print("=" * 45)
print(f"Imágenes procesadas: {imagenes_procesadas}")
print(f"Imágenes aprobadas:  {imagenes_aprobadas}")
print(f"Imágenes a revisar:  {imagenes_procesadas - imagenes_aprobadas}")
print(f"\n📁 Reporte guardado en: {ruta_reporte}")
print("✅ PRÁCTICA TERMINADA EXITOSAMENTE")
# ==========================================
# DATOS DEL ALUMNO
# Nombre: [Tu Nombre Completo]
# Número de Control: [Tu Número de Control] (Terminación 0065)
# ==========================================