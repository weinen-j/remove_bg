try:
    import os
    import rembg
    from PIL import Image
    print("imported")
except Exception as e:
    print(f"{e}")

try:
    import io
    import time
    import logging
except Exception as e:
    print(f"{e}")




#%%
class ImageProcessor:
    def __init__(self, input_folder, output_format, output_quality=None):
        self.input_folder = input_folder
        self.output_format = output_format
        self.output_quality = output_quality
        self.output_folder = os.path.join(input_folder, 'bearbeitet')
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def remove_background(self, img_bytes):
        try:
            return rembg.remove(img_bytes)
        except Exception as e:
            logging.error(f"Error removing background from image: {e}")
            return None

    def crop_image(self, img_bytes):
        try:
            img = Image.open(io.BytesIO(img_bytes))
            mask = img.getchannel('A')
            img = img.crop(mask.getbbox())
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            return img_bytes.getvalue()
        except Exception as e:
            logging.error(f"Error cropping background from image: {e}")
            return None

    def save_image(self, filename, img_bytes):
        try:
            output_file = os.path.join(self.output_folder, os.path.splitext(filename)[0] + '.' + self.output_format)
            with open(output_file, 'wb') as f:
                if self.output_format == 'jpeg':
                    img = Image.open(io.BytesIO(img_bytes))
                    rgb_im = img.convert('RGB')
                    rgb_im.save(f, format=self.output_format, quality=self.output_quality)
                else:
                    f.write(img_bytes)
        except Exception as e:
            logging.error(f"Error saving image: {e}")

    def process_image(self, filename, cropping=False):
        with open(os.path.join(self.input_folder, filename), 'rb') as f:
            img_bytes = f.read()
            img_bytes = self.remove_background(img_bytes)
            if img_bytes is None:
                logging.error(f"Image processing failed for file {filename}")
                return
            if cropping:
                img_bytes = self.crop_image(img_bytes)
                if img_bytes is None:
                    logging.error(f"Image processing failed for file {filename}")
                    return
            self.save_image(filename, img_bytes)

#%%
# Set up the logging configuration


if __name__ == '__main__':
    input_folder = input("Enter the input folder path: ")
    output_format = input("Choose the output image format (JPG or PNG): ").lower()
    while output_format not in ['jpg', 'png', "jpeg"]:
        print("Invalid choice. Please choose JPG or PNG.")
        output_format = input("Choose the output image format (JPG or PNG): ").lower()
        if output_format == "jpg":
            output_format = output_format.replace("jpg", "jpeg")

    if output_format == 'jpeg':
        output_quality = 95
    else:
        output_quality = None

    start_time = time.time()
    log_file = os.path.join(input_folder, 'error.log')
    logging.basicConfig(filename=log_file, level=logging.ERROR)
    processed = []

    processor = ImageProcessor(input_folder, output_format, output_quality)
    cropping = input("Do you want to crop the images? \n y/n: ").lower()
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            processor.process_image(filename, cropping == 'y')
            processed.append(filename)

end_time = time.time()
my_string = '\n'.join(processed)
print(f"Ausgeschnittene Dateien: \n{my_string} \n\nRuntime nach Definition des User-Inputs:", end_time - start_time, "seconds")

a=input("Drücke eine beliebige Taste")