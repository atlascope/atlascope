import io

from django.core.files.uploadedfile import InMemoryUploadedFile


def to_saveable_image(pil_image):
    output_bytes = io.BytesIO()
    pil_image.save(output_bytes, format="PNG")
    output_file = InMemoryUploadedFile(
        output_bytes, None, 'file.png', 'image/png', output_bytes.getbuffer().nbytes, None
    )
    return output_file
