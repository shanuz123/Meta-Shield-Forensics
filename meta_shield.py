import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ExifTags
import os
import math
from PIL.ExifTags import TAGS, GPSTAGS

# Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MetaShieldApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Meta-Shield: EXIF Cleaner")
        self.geometry("900x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_image_path = None
        self.image_data = None

        # Left Panel (Viewer)
        self.viewer_frame = ctk.CTkFrame(self, corner_radius=0, width=300)
        self.viewer_frame.grid(row=0, column=0, sticky="nsew")
        self.viewer_frame.grid_rowconfigure(2, weight=1)

        self.logo_label = ctk.CTkLabel(self.viewer_frame, text="Meta-Shield", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.select_btn = ctk.CTkButton(self.viewer_frame, text="Select Image", command=self.load_image)
        self.select_btn.grid(row=1, column=0, padx=20, pady=10)

        self.image_preview_label = ctk.CTkLabel(self.viewer_frame, text="No Image Selected")
        self.image_preview_label.grid(row=2, column=0, padx=20, pady=10)

        self.file_info_label = ctk.CTkLabel(self.viewer_frame, text="", wraplength=250)
        self.file_info_label.grid(row=3, column=0, padx=20, pady=20)

        # Right Panel (Inspector)
        self.inspector_frame = ctk.CTkFrame(self, corner_radius=0)
        self.inspector_frame.grid(row=0, column=1, sticky="nsew")
        self.inspector_frame.grid_rowconfigure(1, weight=1)
        self.inspector_frame.grid_columnconfigure(0, weight=1)

        self.inspector_title = ctk.CTkLabel(self.inspector_frame, text="Metadata Inspector", font=ctk.CTkFont(size=18, weight="bold"))
        self.inspector_title.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.metadata_textbox = ctk.CTkTextbox(self.inspector_frame, width=500, corner_radius=10)
        self.metadata_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.metadata_textbox.configure(state="disabled")

        self.clean_btn = ctk.CTkButton(self.inspector_frame, text="REMOVE METADATA & SAVE", fg_color="red", hover_color="#AA0000", command=self.clean_image, state="disabled")
        self.clean_btn.grid(row=2, column=0, padx=20, pady=30, sticky="ew")

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.tiff")])
        if not file_path:
            return

        self.current_image_path = file_path
        self.show_image_preview(file_path)
        self.extract_and_show_metadata(file_path)
        self.clean_btn.configure(state="normal")

    def show_image_preview(self, file_path):
        try:
            img = Image.open(file_path)
            # Resize for preview
            img.thumbnail((250, 250))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            
            self.image_preview_label.configure(image=ctk_img, text="")
            
            # File Info
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            filename = os.path.basename(file_path)
            self.file_info_label.configure(text=f"{filename}\n{size_mb:.2f} MB")
            
        except Exception as e:
            self.image_preview_label.configure(image=None, text="Error loading preview")
            print(f"Preview Error: {e}")

    def extract_and_show_metadata(self, file_path):
        self.metadata_textbox.configure(state="normal")
        self.metadata_textbox.delete("1.0", "end")
        
        try:
            img = Image.open(file_path)
            exif_data = img._getexif()
            
            display_text = ""
            
            if not exif_data:
                self.metadata_textbox.insert("0.0", "No EXIF metadata found in this file.\n\nNote: Metadata is often stripped from images downloaded from social media (Facebook, WhatsApp, Twitter).")
                self.metadata_textbox.configure(state="disabled")
                return

            # Helper to get GPS info
            gps_info = None
            for tag, value in exif_data.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_info = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_info[sub_decoded] = value[t]
                    break

            # --- Priority Info ---
            priority_info = ""
            
            # Camera
            make = exif_data.get(271)
            model = exif_data.get(272)
            if make or model:
                priority_info += f"📷 Camera: {make or ''} {model or ''}\n"

            # Date
            date_original = exif_data.get(36867)
            if date_original:
                priority_info += f"📅 Date Taken: {date_original}\n"

            # GPS
            if gps_info:
                lat_dms = gps_info.get("GPSLatitude")
                lat_ref = gps_info.get("GPSLatitudeRef")
                lon_dms = gps_info.get("GPSLongitude")
                lon_ref = gps_info.get("GPSLongitudeRef")
                
                if lat_dms and lat_ref and lon_dms and lon_ref:
                    try:
                        lat = self.convert_to_degrees(lat_dms)
                        if lat_ref != "N": lat = -lat
                        
                        lon = self.convert_to_degrees(lon_dms)
                        if lon_ref != "E": lon = -lon
                        
                        priority_info += f"📍 GPS Coordinates:\n   Lat: {lat:.6f}, Lon: {lon:.6f}\n"
                        priority_info += f"   (Link: https://maps.google.com/?q={lat},{lon})\n"
                    except ValueError as ve:
                        # Specific handling for our own "invalid/NaN" error
                        priority_info += f"📍 GPS Tag detected, but values are invalid/empty (NaN).\n   (Likely scrubbed by privacy software like Snapseed)\n"
                    except Exception as e:
                         priority_info += f"📍 GPS found but error parsing: {e}\n"
            
            # --- Diagnostic Hint if GPS is missing but Camera is present ---
            elif (make or model) and not gps_info:
                 priority_info += "\n⚠ GPS INFO MISSING\n   Camera data found, but location is absent.\n   Possible causes:\n   - 'Save Location' disabled in Camera settings.\n   - Image transferred via WhatsApp/Phone Link (strips metadata).\n"

            if priority_info:
                display_text += "--- KEY METADATA ---\n" + priority_info + "\n"
            
            # --- All Metadata ---
            display_text += "--- ALL DETECTED TAGS ---\n"
            count = 0
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                # Skip long binary data or MakerNotes for readability
                if tag_name == "MakerNote" or tag_name == "UserComment":
                    value = "<Binary/Long Data Omitted>"
                
                display_text += f"{tag_name}: {value}\n"
                count += 1
                
            self.metadata_textbox.insert("0.0", display_text)
            
        except Exception as e:
            self.metadata_textbox.insert("0.0", f"Error extracting metadata: {e}")
            print(f"DEBUG Error: {e}")
            
        self.metadata_textbox.configure(state="disabled")

    def convert_to_degrees(self, value):
        """Helper to convert DMS (Degrees, Minutes, Seconds) to Decimal."""
        def get_float(x):
            try:
                # Handle Pillow IFDRational if needed
                if hasattr(x, 'numerator') and hasattr(x, 'denominator'):
                    if x.denominator == 0:
                        return float('nan')
                    return float(x.numerator) / float(x.denominator)
                return float(x)
            except (ZeroDivisionError, ValueError, TypeError):
                return float('nan')

        d = get_float(value[0])
        m = get_float(value[1])
        s = get_float(value[2])
        
        if math.isnan(d) or math.isnan(m) or math.isnan(s):
             raise ValueError("Contains invalid or NaN GPS data")

        return d + (m / 60.0) + (s / 3600.0)

    def clean_image(self):
        if not self.current_image_path:
            return
            
        try:
            img = Image.open(self.current_image_path)
            
            # Create a new filename
            base, ext = os.path.splitext(self.current_image_path)
            new_path = f"{base}_clean{ext}"
            
            # We strip metadata by creating a new image without the exif dict
            data = list(img.getdata())
            img_no_exif = Image.new(img.mode, img.size)
            img_no_exif.putdata(data)
            
            # Save
            img_no_exif.save(new_path)
            
            messagebox.showinfo("Success", f"Metadata removed!\nSaved as: {os.path.basename(new_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clean image: {e}")

if __name__ == "__main__":
    app = MetaShieldApp()
    app.mainloop()
