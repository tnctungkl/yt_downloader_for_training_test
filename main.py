from pytube import YouTube
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, filedialog, PhotoImage
from threading import Thread
from fpdf import FPDF
import os
import pytube


class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("[TEST FOR LEARNING]YouTube Downloader")

        self.logo_image_yt = PhotoImage(file="logos/youtube.png")
        self.logo_label_1 = Label(root, image=self.logo_image_yt)
        self.logo_label_1.pack()

        self.url_label = Label(root, text="YouTube URL:")
        self.url_label.pack()

        self.url_var = StringVar()
        self.url_entry = Entry(root, textvariable=self.url_var, width=75)
        self.url_entry.pack()

        self.logo_image_drctry = PhotoImage(file="logos/folder.png")
        self.logo_label_2 = Label(root, image=self.logo_image_drctry)
        self.logo_label_2.pack()

        self.directory_label = Label(root, text="Save Directory:")
        self.directory_label.pack()

        self.directory_var = StringVar()
        self.directory_entry = Entry(root, textvariable=self.directory_var, width=75)
        self.directory_entry.pack()

        self.browse_button = Button(root, text="Save", command=self.browse_directory)
        self.browse_button.pack()

        self.download_button = Button(root, text="Download", command=self.download)
        self.download_button.pack()

    def browse_directory(self):
        selected_dir = filedialog.askdirectory()
        self.directory_var.set(selected_dir)

    def download(self):
        url = self.url_var.get()
        save_dir = self.directory_var.get()

        if not url or not save_dir:
            messagebox.showerror("Error: ", "Please, provide URL and save directory!")
            return

        try:
            youtube = pytube.YouTube(url)
            video_stream = youtube.streams.get_highest_resolution()

            def format_video_length(length_in_seconds):
                hours, remainder = divmod(length_in_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{hours:02}:{minutes:02}:{seconds:02}"

            def format_view_count(views):
                if views >= 1000000:
                    return f"{views // 1000000} Million {views % 1000000 // 1000} Thousand {views % 1000} times"
                elif views >= 1000:
                    return f"{views // 1000} Thousand {views % 1000} times"
                else:
                    return f"{views} times"

            def download_thread():
                try:
                    video_stream.download(output_path=save_dir)
                    messagebox.showinfo("Success!", "Download Complete!")

                    video_info = {
                        "Video Title": youtube.title,
                        "Video Owner": youtube.author,
                        "Thumbnail Image": youtube.thumbnail_url,
                        "Video Description": youtube.description,
                        "Video Length": format_video_length(youtube.length),
                        "Video Rating": youtube.rating,
                        "View Count": format_view_count(youtube.views)
                    }

                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, "Video Metadata", ln=True, align="C")
                    pdf.ln(10)
                    for key, value in video_info.items():
                        pdf.cell(0, 10, f"{key}: {value}", ln=True)
                    pdf_file_path = os.path.join(save_dir, f"{youtube.title}_metadata.pdf")
                    pdf.output(pdf_file_path)

                    messagebox.showinfo("Success!", "Download, Metadata Extraction, and Subtitles Extraction Complete!")

                    self.url_var.set('')
                    self.directory_var.set('')

                except Exception as e:
                    messagebox.showerror("Error: ", f"An Error Occurred: {str(e)}")

            download_thread_instance = Thread(target=download_thread)
            download_thread_instance.start()

        except Exception as e:
            messagebox.showerror("Error: ", f"An Error Occurred: {str(e)}")


def main():
    root = Tk()
    app = YouTubeDownloader(root)
    root.mainloop()


if __name__ == "__main__":
    main()
