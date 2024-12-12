import os
import matplotlib.pyplot as plt
from db import get_connection,get_images_info

def main():
    """Vis."""
    # print justificado
    # "Visual graf"
    conn=get_connection('config.ini')
    info=get_images_info(conn)
    # Conteo por cat
    from collections import Counter
    c=Counter(info.values())
    categorias=list(c.keys())
    cantidades=list(c.values())
    fig,ax=plt.subplots()
    ax.bar(categorias,cantidades,color='skyblue')
    ax.set_title('Cantidad de imágenes por categoría')
    ax.set_xlabel('Categoría')
    ax.set_ylabel('Cantidad')
    plt.tight_layout()
    vis_dir=os.path.join(os.path.dirname(__file__),'..','visualizaciones')
    if not os.path.exists(vis_dir):
        os.makedirs(vis_dir)
    out_path=os.path.join(vis_dir,'imagenes_por_categoria.png')
    plt.savefig(out_path)
    plt.close()
    conn.close()
    print(f"Visualización generada en: {out_path}")

if __name__=='__main__':
    main()
