from django.core.exceptions import ValidationError
from PIL import Image

def validate_image_size_only(image):
    max_size_mb = 5
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError("El archivo es demasiado grande. El tamaño máximo permitido es de %(max_size_mb)s MB.",
                              params={'max_size_mb': max_size_mb})

def validate_image_size_and_dimensions(image):
    max_size_mb = 1
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError("El archivo es demasiado grande. El tamaño máximo permitido es de %(max_size_mb)s MB.",
                              params={'max_size_mb': max_size_mb})

    img = Image.open(image)
    width, height = img.size
    if not ((width == 256 and height == 256) or (width == 512 and height == 512)):
        raise ValidationError("La imagen debe tener dimensiones de 256x256 o 512x512 píxeles.")

def validate_file_size(file):
    max_size_mb = 10
    allowed_extensions = ['pdf', 'xls', 'xlsx']
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError("El archivo es demasiado grande. El tamaño máximo permitido es de %(max_size_mb)s MB.",
                              params={'max_size_mb': max_size_mb})

    if not file.name.split('.')[-1].lower() in allowed_extensions:
        raise ValidationError(f'El archivo debe tener alguna de estas extensiones: {", ".join(allowed_extensions)}.')
