import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDFS_DIR = os.path.join(BASE_DIR, "pdfs")
os.makedirs(PDFS_DIR, exist_ok=True)

def generar_pdf(productos, nombre_archivo="catalogo.pdf"):
    ruta_pdf = os.path.join(PDFS_DIR, nombre_archivo)
    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
    elementos = []
    estilos = getSampleStyleSheet()

    # 🔹 Estilo para texto de celdas con justificación
    estilos.add(ParagraphStyle(
        name="TablaTexto",
        fontSize=9,
        leading=11,
        alignment=4   # 4 = Justify
    ))

    elementos.append(Paragraph("Factura / Pedido", estilos["Title"]))
    elementos.append(Spacer(1, 12))

    # Encabezados
    data = [["Producto", "Laboratorio", "Cantidad", "Precio", "Subtotal"]]
    total = 0
    for p in productos:
        cantidad = int(p.get("cantidad", 1) or 0)
        precio = float(p.get("precio", 0) or 0)
        subtotal = cantidad * precio
        total += subtotal

        # 🔹 Usamos Paragraph para que el texto se ajuste y se justifique
        producto = Paragraph(p.get("nombre", ""), estilos["TablaTexto"])
        laboratorio = Paragraph(p.get("laboratorio", ""), estilos["TablaTexto"])

        data.append([
            producto,
            laboratorio,
            str(cantidad),
            f"${precio:,.2f}",
            f"${subtotal:,.2f}"
        ])

    # Fila total
    data.append(["", "", "", "TOTAL", f"${total:,.2f}"])

    # Ajustamos anchos
    tabla = Table(data, colWidths=[220, 120, 50, 60, 70])

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#003399")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("VALIGN", (0,0), (-1,-1), "TOP"),   # texto alineado arriba
        ("ALIGN", (2,1), (2,-2), "CENTER"),  # cantidad centrada
        ("ALIGN", (3,1), (4,-2), "RIGHT"),   # precios a la derecha
    ]))

    elementos.append(tabla)
    doc.build(elementos)
    return ruta_pdf




