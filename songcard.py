import flet as ft
import yt_dlp as yt


class SongCard(ft.Column):
    def __init__(self, text: str, url: str, destination: str):
        super().__init__()
        self.width = 350
        self.height = 75
        self.color = ft.Colors.GREY_700
        self.radius = 20
        self.text = text
        self.url = url
        self.destination = destination
        self.controls = [ft.Container(
            width=self.width,
            height=self.height,
            border_radius=ft.border_radius.all(self.radius),
            bgcolor=self.color,
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.LINK,
                        on_click=self.__redirect_song,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Text(
                        value=self.__truncate(self.text),
                        weight=ft.FontWeight.BOLD,
                        size=10,
                        expand=True,
                        font_family="Montserrat"
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DOWNLOAD,
                        on_click=self.__download_song,
                    ),
                ]
            ),
            padding=10,
        )]

    async def __redirect_song(self, e):
        await self.page.launch_url(self.url)

    def __download_song(self, e):
        def close_path(e):
            dialog_path.open=False
            e.page.update()

        if self.destination == "None":
            dialog_path = ft.AlertDialog(
                modal=True,
                title=ft.Text("Error"),
                content=ft.Text("There isn't any path defined or an error occurred"),
                actions=[ft.TextButton("Close", on_click=close_path)]
            )
            e.page.overlay.append(dialog_path)
            dialog_path.open = True
        else:
            page = e.page
            def close_success(e):
                dialog_success.open = False
                page.update()

            def close_error(e):
                dialog_error.open = False
                page.update()

            progress_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"Downloading {self.text}", size=15),
                content=ft.Container(content=ft.ProgressRing(), padding=20, alignment=ft.Alignment.CENTER, height=100)
            )

            dialog_success = ft.AlertDialog(
                modal=True,
                title=ft.Text("Download Complete"),
                content=ft.Text(f"Finished downloading: {self.text}"),
                actions=[ft.TextButton("OK", on_click=close_success)]
            )

            dialog_error = ft.AlertDialog(
                modal=True,
                title=ft.Text("Error"),
                content=ft.Text("There isn't any path defined or an error occurred"),
                actions=[ft.TextButton("Close", on_click=close_error)]
            )

            page.overlay.extend([progress_dialog, dialog_success, dialog_error])
            progress_dialog.open = True
            page.update()

            def run_download():
                ydl_opts = {
                    'format': 'bestaudio[ext=m4a]/bestaudio',
                    'quiet': True,
                    'outtmpl': f'{self.get_fixed_destination(self.destination)}%(title)s.%(ext)s',
                    'noplaylist': True,
                }

                try:
                    with yt.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([self.url])
                    page.update()
                    progress_dialog.open = False
                    dialog_success.open = True


                except Exception as ex:
                    print(f"Error descargando: {ex}")
                    progress_dialog.open = False
                    dialog_error.content = ft.Text(f"Error: {str(ex)}")
                    dialog_error.open = True

                finally:
                    page.update()

            run_download()


    @staticmethod
    def __truncate(text: str):
        if len(text)<=70:
            return text
        else:
            return text[:70] + "..."

    def get_fixed_destination(self, destination: str) -> str:
        if destination.endswith("/"):
            return destination
        else:
            return destination + "/"