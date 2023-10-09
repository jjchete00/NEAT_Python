

from PIL import Image

# Open the image file
image = Image.open('imagenes/45908.jpg')  # Replace 'input_image.jpg' with your image file path

# Resize the image to 50x50 pixels
resized_image = image.resize((1100, 700))

# Save the resized image to a file
resized_image.save('imagenes/background2.jpg')  