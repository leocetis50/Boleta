import flet as ft
import csv
import os

def main(page: ft.Page):
    page.title = "Boleta de calificaciones"
    page.bgcolor = ft.Colors.BLUE_ACCENT_700
    page.window_height = 600

    lista_alumnos = ft.Dropdown(
        width=200,
        label="Alumnos",
        options=[
            ft.dropdown.Option("Leonardo Cesar Martinez Martinez"),
            ft.dropdown.Option("Ismael Macias Pérez"),
            ft.dropdown.Option("Ayari Zoe Cosme Rodriguez"),
            ft.dropdown.Option("Santiago Bello Perez"),
            ft.dropdown.Option("Erick David Ruiz Rodriguez"),
            ft.dropdown.Option("Batsabeth Guzman Tellez")
        ],
    )

    def crear_dropdown(materia):
        return ft.Dropdown(
            width=150,
            label=materia,
            options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
        )

    esp = crear_dropdown("Español")
    mat = crear_dropdown("Matemáticas")
    ing = crear_dropdown("Inglés")
    info = crear_dropdown("Informática")
    hist = crear_dropdown("Historia")
    hum = crear_dropdown("Humanidades")
    eco = crear_dropdown("Ecosistemas")

    label_promedio = ft.Text(value="", size=20, width=100, color="white")

    tabla_calificaciones = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Alumno")),
            ft.DataColumn(label=ft.Text("Español")),
            ft.DataColumn(label=ft.Text("Matemáticas")),
            ft.DataColumn(label=ft.Text("Inglés")),
            ft.DataColumn(label=ft.Text("Informática")),
            ft.DataColumn(label=ft.Text("Historia")),
            ft.DataColumn(label=ft.Text("Humanidades")),
            ft.DataColumn(label=ft.Text("Ecosistemas")),
            ft.DataColumn(label=ft.Text("Promedio")),
            ft.DataColumn(label=ft.Text("Desempeño")),
        ],
        rows=[]
    )

    def obtener_color(promedio):
        if promedio < 60:
            return ft.Container(width=20, height=20, bgcolor="red", border_radius=50)
        elif promedio < 80:
            return ft.Container(width=20, height=20, bgcolor="yellow", border_radius=50)
        else:
            return ft.Container(width=20, height=20, bgcolor= ft.Colors.GREEN_ACCENT_400, border_radius=50)

    def obtener_desempeno_texto(promedio):
        if promedio < 60:
            return "Malo"
        elif promedio < 80:
            return "Bueno"
        else:
            return "Muy Bueno"

    def calcular_promedio(e):
        alumno = lista_alumnos.value
        if not alumno:
            page.snack_bar = ft.SnackBar(ft.Text("Debes seleccionar un alumno."))
            page.snack_bar.open = True
            page.update()
            return

        notas = [
            int(esp.value or 0),
            int(mat.value or 0),
            int(ing.value or 0),
            int(info.value or 0),
            int(hist.value or 0),
            int(hum.value or 0),
            int(eco.value or 0),
        ]
        promedio = sum(notas) / len(notas)
        label_promedio.value = f"{promedio:.2f}"

        color = obtener_color(promedio)
        desempeno_texto = obtener_desempeno_texto(promedio)

        for row in tabla_calificaciones.rows:
            if row.cells[0].content.value == alumno:
                row.cells[1].content.value = esp.value or ""
                row.cells[2].content.value = mat.value or ""
                row.cells[3].content.value = ing.value or ""
                row.cells[4].content.value = info.value or ""
                row.cells[5].content.value = hist.value or ""
                row.cells[6].content.value = hum.value or ""
                row.cells[7].content.value = eco.value or ""
                row.cells[8].content.value = f"{promedio:.2f}"
                row.cells[9].content = color
                row.cells[9].content.data = desempeno_texto  
                page.snack_bar = ft.SnackBar(ft.Text(f"Calificaciones actualizadas para {alumno}."))
                page.snack_bar.open = True
                page.update()
                return

        nueva_fila = ft.DataRow(cells=[
            ft.DataCell(ft.Text(alumno)),
            ft.DataCell(ft.Text(esp.value or "")),
            ft.DataCell(ft.Text(mat.value or "")),
            ft.DataCell(ft.Text(ing.value or "")),
            ft.DataCell(ft.Text(info.value or "")),
            ft.DataCell(ft.Text(hist.value or "")),
            ft.DataCell(ft.Text(hum.value or "")),
            ft.DataCell(ft.Text(eco.value or "")),
            ft.DataCell(ft.Text(f"{promedio:.2f}")),
            ft.DataCell(ft.Container(content=color.content, bgcolor=color.bgcolor, width=20, height=20, border_radius=50, data=desempeno_texto)),
        ])
        tabla_calificaciones.rows.append(nueva_fila)
        page.snack_bar = ft.SnackBar(ft.Text(f"Alumno {alumno} agregado correctamente."))
        page.snack_bar.open = True
        page.update()

    def borrar_alumno(e):
        alumno = lista_alumnos.value
        if not alumno:
            page.snack_bar = ft.SnackBar(ft.Text("Selecciona un alumno para borrar."))
            page.snack_bar.open = True
            page.update()
            return

        encontrado = False
        for i, row in enumerate(tabla_calificaciones.rows):
            if row.cells[0].content.value == alumno:
                del tabla_calificaciones.rows[i]
                encontrado = True
                break

        if encontrado:
            page.snack_bar = ft.SnackBar(ft.Text(f"Alumno {alumno} eliminado correctamente."))
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"El alumno {alumno} no está en la tabla."))
        page.snack_bar.open = True
        page.update()

    def borrar_todo(e):
        if not tabla_calificaciones.rows:
            page.snack_bar = ft.SnackBar(ft.Text("No hay registros para borrar."))
        else:
            tabla_calificaciones.rows.clear()
            page.snack_bar = ft.SnackBar(ft.Text("Todos los registros han sido eliminados."))
        page.snack_bar.open = True
        page.update()

    def exportar_csv(e):
        if not tabla_calificaciones.rows:
            page.snack_bar = ft.SnackBar(ft.Text("No hay datos para exportar."))
            page.snack_bar.open = True
            page.update()
            return

        archivo = "boleta.csv"
        encabezados = ["Alumno", "Español", "Matemáticas", "Inglés", "Informática",
                       "Historia", "Humanidades", "Ecosistemas", "Promedio", "Desempeño"]

        with open(archivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(encabezados)
            for row in tabla_calificaciones.rows:
                datos = [cell.content.value if hasattr(cell.content, "value") else "" for cell in row.cells[:-1]]

                desempeno_texto = row.cells[9].content.data if hasattr(row.cells[9].content, "data") else ""
                datos.append(desempeno_texto)
                writer.writerow(datos)

        page.snack_bar = ft.SnackBar(ft.Text(f"Datos exportados correctamente a '{os.path.abspath(archivo)}'"))
        page.snack_bar.open = True
        page.update()

    boton_calcular = ft.ElevatedButton(text="Calcular Promedio",color="white", on_click=calcular_promedio)
    boton_borrar = ft.ElevatedButton(text="Borrar Alumno", color="white", bgcolor="black", on_click=borrar_alumno)
    boton_borrar_todo = ft.ElevatedButton(text="Borrar Todo", color="white", bgcolor="black", on_click=borrar_todo)
    boton_exportar = ft.ElevatedButton(text="Exportar CSV", color="white", bgcolor="black", on_click=exportar_csv)

    fila_dropdowns = ft.Row(
        [
            lista_alumnos,
            esp,
            mat,
            ing,
            info,
            hist,
            hum,
            eco,
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )

    fila_botones = ft.Row(
        [boton_calcular, boton_borrar, boton_borrar_todo, boton_exportar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    page.add(
        ft.Column(
            [
                fila_dropdowns,
                fila_botones,
                tabla_calificaciones
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
    )

ft.app(target=main, view=ft.WEB_BROWSER)