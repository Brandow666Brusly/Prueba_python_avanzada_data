def imprimir_log(presentes, ausentes, no_catalogadas, info):
    """
    Imprime el log final de la migración.
    info: dict {nombre_archivo: categoria}
    """
    print("===== LOG DE MIGRACIÓN =====")

    # Presente
    print("\n*** Imágenes Presentes (En BD y FS) ***")
    for img in sorted(presentes):
        categoria = info.get(img, 'Desconocida')
        print(f"Imagen: {img} | Categoría: {categoria} | Estado: Presente")

    # Ausente
    print("\n*** Imágenes Ausentes (En BD pero no en FS) ***")
    for img in sorted(ausentes):
        categoria = info.get(img, 'Desconocida')
        print(f"Imagen: {img} | Categoría: {categoria} | Estado: Ausente")

    # No catalogada
    print("\n*** Imágenes No Catalogadas (En FS pero no en BD) ***")
    for img in sorted(no_catalogadas):
        print(f"Imagen: {img} | Categoría: No disponible | Estado: No catalogada")

    print("\n===== FIN DEL LOG DE MIGRACIÓN =====")