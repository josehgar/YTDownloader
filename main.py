import flet as ft
import yt_dlp as yt
import json, os, stat, shutil
from songcard import SongCard
import flet_permission_handler as fph

download_path="None"
json_file="config.json"


async def main(page: ft.Page) -> None:
    p_handler = fph.PermissionHandler()
    result = await p_handler.request(fph.Permission.MANAGE_EXTERNAL_STORAGE)
    print(f"Resultado: {result}")
    if result == fph.PermissionStatus.GRANTED:
        page.snack_bar = ft.SnackBar(content=ft.Text("Permiso concedido ✓"))
        page.snack_bar.open = True
        page.update()
    else:
        page.snack_bar = ft.SnackBar(content=ft.Text("Permiso denegado, abre ajustes"))
        page.snack_bar.open = True
        page.update()
        await p_handler.open_app_settings()
    global download_path
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            data=json.load(f)
            download_path=data["download_path"]
    page.title="Youtube Downloader MP3"
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.window.width=500
    page.window.height=800
    page.bgcolor=ft.Colors.GREY_900
    page.fonts={
        "Montserrat": "Montserrat-VariableFont_wght.ttf"
    }

    file_picker=ft.FilePicker()
    path_text=ft.Text(
        spans=[
            ft.TextSpan("Download path: ", ft.TextStyle(color=ft.Colors.WHITE, font_family="Montserrat")),
            ft.TextSpan(
                text="None" if download_path == "None" else download_path,
                style=ft.TextStyle(color=ft.Colors.RED_400, font_family="Montserrat") if download_path == "None" else ft.TextStyle(color=ft.Colors.GREEN_400, font_family="Montserrat")
            )
        ],
        align=ft.Alignment.TOP_LEFT,
    )

    async def set_path(e):
        global download_path
        ruta_seleccionada=await file_picker.get_directory_path()
        if ruta_seleccionada:
            download_path = ruta_seleccionada
            path_text.spans[1].text = download_path
            path_text.spans[1].style = ft.TextStyle(color=ft.Colors.GREEN_400)
        else:
            download_path = "None"
            path_text.spans[1].text = "None"
            path_text.spans[1].style = ft.TextStyle(color=ft.Colors.RED_400)
        for song in song_list.controls:
            if isinstance(song, SongCard):
                song.destination = download_path
        with open(json_file, 'w') as f:
            json.dump({"download_path": download_path}, f)
        page.update()

    def search_query(e):
        query=e.control.value
        if not query:
            return

        song_list.controls.clear()

        ydl_opts = {
            "quiet": False,
            "skip_download": True,
            "no_playlist": True,
            'extract_flat': True
        }

        with yt.YoutubeDL(ydl_opts) as ydl:
            busqueda=f"ytsearch5:{query}"
            info=ydl.extract_info(busqueda, download=False)
            entries = info.get("entries", [])

            song_list.controls.clear()

            if not entries:
                song_list.controls.append(
                    ft.Text("No videos found")
                )
            else:
                for song in entries:
                    url = song.get("url")
                    duration = song.get("duration")

                    if "youtube.com/channel/" in url or "youtube.com/@" in url:
                        continue

                    if duration is None:
                        continue

                    titulo = song.get("title")
                    song_list.controls.append(SongCard(titulo, url, download_path))

            page.update()

    song_list=ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(
        ft.Column(
            spacing=25,
            expand=True,
            controls=[
                ft.Divider(height=75, color="transparent"),
                path_text,
                ft.Row(
                    spacing=40,
                    controls=[
                        ft.Container(
                            content=ft.Text(
                            text_align=ft.TextAlign.CENTER,
                            value="YTDownloader",
                            size=30,
                            font_family="Montserrat",
                            weight=ft.FontWeight.BOLD,
                            ),
                        ),

                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Button(
                            content="Set path",
                            icon_color=ft.Colors.GREY_800,
                            on_click=set_path
                            ),
                            padding=50
                        )

                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            text_align=ft.TextAlign.LEFT,
                            value="Search any song from YouTube",
                            font_family="Montserrat",
                            size=15
                        ),
                        ft.TextField(
                            align=ft.Alignment.CENTER,
                            hint_text="Search...",
                            bgcolor=ft.Colors.GREY_800,
                            border_width=0,
                            width=350,
                            height=70,
                            on_submit=search_query
                        ),
                        song_list
                    ]
                )
            ]
        )
    )

ft.run(main, assets_dir="assets")