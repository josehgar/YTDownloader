import flet as ft
import yt_dlp as yt
from mutagen.mp4 import MP4, MP4Cover
import requests


class SongCard(ft.Column):
    def __init__(self, text: str, url: str, destination: str):
        super().__init__()
        self.width = 350
        self.height = 75
        self.color = ft.Colors.GREY_700
        self.radius = 20
        self.text = text
        self.url = url # Url is passed as parameter to manage the video URL from all points of the project
        self.destination = destination # Same as url, but with the download path
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

    # It redirects to the original YouTube video
    async def __redirect_song(self, e):
        await self.page.launch_url(self.url)

    # Manages the download process and AlertDialogs
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

            progress_dialog.open = True
            page.overlay.extend([progress_dialog, dialog_success, dialog_error])
            page.update()

            # Crops the image to a squared format
            def crop_to_square(image_bytes: bytes) -> bytes:
                from PIL import Image
                import io

                img = Image.open(io.BytesIO(image_bytes))
                w, h = img.size
                size = min(w, h)

                # Crop centrado
                left = (w - size) // 2
                top = (h - size) // 2
                img_cropped = img.crop((left, top, left + size, top + size))

                output = io.BytesIO()
                img_cropped.save(output, format="JPEG", quality=95)
                return output.getvalue()

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

                        # It writes metadata from YouTube into the .m4a file
                        info=ydl.extract_info(self.url, download=True)
                        file_path = f'{self.get_fixed_destination(self.destination)}{info["title"]}.m4a'
                        audio=MP4(file_path)
                        audio['\xa9nam'] = [info.get('title', '')]
                        audio['\xa9ART'] = [info.get('uploader', '')]
                        audio['\xa9day'] = [info.get('upload_date', '')[:4]]
                        audio['\xa9cmt'] = [info.get('description', '')]
                        thumbnail_url = info.get('thumbnail')
                        if thumbnail_url:
                            img_data = requests.get(thumbnail_url).content
                            img_data = crop_to_square(img_data)
                            audio['covr'] = [MP4Cover(img_data, imageformat=MP4Cover.FORMAT_JPEG)]

                        audio.save()
                    progress_dialog.open=False
                    page.update()
                    dialog_success.open = True
                    page.update()


                except Exception as ex:
                    progress_dialog.open = False
                    page.update()
                    dialog_error.content = ft.Text(f"Error: {str(ex)}")
                    dialog_error.open = True

                finally:
                    page.update()

            e.page.run_thread(run_download) # Used Flet thread method (the one from 'threading' class gives problems)


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