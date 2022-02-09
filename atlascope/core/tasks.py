import imp
import io

from PIL import Image
from celery import shared_task
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
# from s3_file_field.widgets import S3PlaceholderFile

from atlascope.core.models import Dataset, JobScript


@shared_task
def spawn_job(job_data):
    # celery arguments must be serializable
    original_dataset = Dataset.objects.get(
        id=job_data['original_dataset']
        )
    job_script = JobScript.objects.get(id=job_data['script'])
    script = job_script.script_contents.read()
    # input_image_placeholder = S3PlaceholderFile.from_field(job_data['input_image'])
    # print(job_data['input_image'])
    # input_image = Image.open(io.BytesIO(
    #     job_data['input_image']
    # ))
    # TODO: use job data region to extract sub image
    input_image = Image.open(io.BytesIO(original_dataset.content.read()))
    kwargs = job_data['additional_inputs'] or {}

    # TODO: sandbox this
    module = imp.new_module('main')
    exec(script, module.__dict__)
    output_dict = module.main(input_image=input_image, **kwargs)

    def interpret_output(key, output):
        if not isinstance(output, Image.Image):
            return output
        else:
            return store_image(output, key)

    def store_image(image, output_key):
        filename = f'{original_dataset.name.replace(" ", "_")+"_"}'\
            f'{job_script.name.replace(" ", "_")}_image_output_{output_key}.png'
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_file = InMemoryUploadedFile(
            image_bytes,
            None,
            filename,
            'image/png',
            image_bytes.getbuffer().nbytes,
            None,
        )

        return image_file

    print({key: interpret_output(key, output) for key, output in output_dict.items()})
    print(timezone.now())
