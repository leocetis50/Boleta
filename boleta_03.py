import flet as ft 

def main(page: ft.Page):
    page.title = "Boleta de Calificaciones"
    page.bgcolor = ft.Colors.GREEN_ACCENT_400
    page.window_width = 1600
    page.window_height = 600
    
    lista_alumnos = ft.Dropdown(
        width = 300,
        label = "Alumnos",
        options = [
            ft.dropdown.Option("Ismael Macias Perez"),
            ft.dropdown.Option("Ayari Cosme Rodriguez"),
            ft.dropdown.Option("Leonardo Martinez Martinez"),
            ft.dropdown.Option("Betsabeth Guzman Tellez"),
            ft.dropdown.Option("Elisabeth"),
            ft.dropdown.Option("Santiago Bello Perez"),
            ],
    )

    esp = ft.Dropdown(width=150,label="Español",
                  options=[ft.dropdown.Option(str(i)) for i in range(10,101,10)])
    mat = ft.Dropdown(width=150,label="Matematicas",
                  options= [ft.dropdown.Option(str(i)) for i in range(10,101,10)])
    ing = ft.Dropdown(width=150,label="Ingles",
                  options=[ft.dropdown.Option(str(i)) for i in range (10,101,10)])
    info = ft.Dropdown(width=150, label= "Informatica",
                   options=[ft.dropdown.Option(str(i)) for i in range (10,101,10)])
    hist = ft.Dropdown(width=150,label="Historia",
                   options=[ft.dropdown.Option(str(i)) for i in range(10,101,10)])
    quim = ft.Dropdown(width=150,label= "Quimica",
                   options=[ft.dropdown.Option(str(i)) for i in range(10,101,10)])
    huma = ft.Dropdown(width=150,label="Humanidades",
                   options=[ft.dropdown.Option(str(i)) for i in range(10,101,10)])

    label_promedio = ft.Text(value="", size=20, width=100, color="WHITE")

    tabla_calificaciones = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Alumno")),
            ft.DataColumn(label=ft.Text("Español")),
            ft.DataColumn(label=ft.Text("Matematicas")),
            ft.DataColumn(label=ft.Text("Ingles")),
            ft.DataColumn(label=ft.Text("Ingles")),
            ft.DataColumn(label=ft.Text("Informatica")),
            ft.DataColumn(label=ft.Text("Quimica")),
            ft.DataColumn(label=ft.Text("Humanidades")),
            ft.DataColumn(label=ft.Text("Promedio")),
        ],
        rows=[]
    )
    def calcular_promedio(e):
        notas = [
            int(esp.value or 0),
            int(mat.value or 0),
            int(ing.value or 0),
            int(info.value or 0),
            int(hist.value or 0),
            int(quim.value or 0),
            int(huma.value or 0)
        ]
        promedio = sum(notas) / len(notas)
        label_promedio.value = f"{promedio:.2f}"

        nueva_fila = ft.DataRow(cells=[
            ft.DataCell(ft.Text(lista_alumnos.value or "")),
            ft.DataCell(ft.Text(esp.value or"")),
            ft.DataCell(ft.Text(mat.value or"")),
            ft.DataCell(ft.Text(ing.value or"")),
            ft.DataCell(ft.Text(info.value or"")),
            ft.DataCell(ft.Text(hist.value or"")),
            ft.DataCell(ft.Text(quim.value or"")),
            ft.DataCell(ft.Text(huma.value or"")),
            ft.DataCell(ft.Text(f"{promedio:.2f}")),        
        ])
        tabla_calificaciones.rows.append(nueva_fila)
        page.update()
    
    boton_calcular = ft.ElevatedButton(text="Calcular Promedio", on_click=calcular_promedio)
    #boton_borrar = ft.ElevatedButton(text="Borrar" on_click=)
    fila_dropdowns = ft.Row(
        [
            lista_alumnos,
            esp,     
            mat, 
            ing,
            info, 
            hist,
            quim,
            huma,
            label_promedio
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )
    fila_boton = ft.Row(
        [boton_calcular],
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(
        ft.Column(
            [
                fila_dropdowns,
                fila_boton,
                tabla_calificaciones
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
    )
        
        
ft.app(target=main, view=ft.WEB_BROWSER)