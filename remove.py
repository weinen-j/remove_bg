import os
import rembg
from PIL import Image
import io
import time

start_time = time.time()
# conda remove -n ENV_NAME --all
# conda create -n envname python=x.x

# prompt the user to enter the input folder path
input_folder = input("Enter the input folder path: ")
cropping = input("Do you want to crop the images? \n y/n: ").lower()


# create the output folder by adding /bearbeitet to the input folder path
output_folder = os.path.join(input_folder, 'bearbeitet')

# create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# prompt the user to choose the output image format
while True:
    output_format = input("Choose the output image format (JPEG or PNG): ").lower()
    if output_format in ['jpeg', 'png']:
        break
    else:
        print("Invalid choice. Please choose JPEG or PNG.")

# set the JPEG quality to 95 if JPEG is chosen as the output format
if output_format == 'jpeg':
    output_quality = 95
else:
    output_quality = None


# loop through all the files in the input folder
for filename in os.listdir(input_folder):
    # check if the file is an image (ends with .jpg, .jpeg, or .png)
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        # load the image and remove the background using rembg
        with open(os.path.join(input_folder, filename), 'rb') as f:
            img_bytes = f.read()
            img = rembg.remove(img_bytes)
            if cropping == "y":
                # convert the bytes to a PIL Image
                img = Image.open(io.BytesIO(rembg.remove(img_bytes)))
                # get the bounding box of the foreground
                mask = img.getchannel('A')
                # crop the image based on the bounding box
                img = img.crop(mask.getbbox())

        # convert the image to the specified output format and save to the output folder
        output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + '.' + output_format)
        with open(output_file, 'wb') as f:
            if output_format == 'jpeg':
                # convert the bytes to a PIL Image and save as JPEG with the specified quality
                if isinstance(img, Image.Image):
                    pass
                else:
                    img = Image.open(io.BytesIO(img))
                rgb_im = img.convert('RGB')
                rgb_im.save(f, format=output_format, quality=output_quality)
            else:
                # write the bytes directly to the output file for PNG format
                f.write(img)

end_time = time.time()
print("Runtime:", end_time - start_time, "seconds")
