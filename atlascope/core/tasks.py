from celery import shared_task
import imp
import io
from PIL import Image

from django.utils import timezone
from atlascope.core.models import Job


class ImageStorageBuffer:
    def __init__(self, image_bytes):
        self.image_bytes = image_bytes

    def read(self, length):
        return self.image_bytes.getvalue()


@shared_task
def spawn_job(job_id):
    # celery arguments must be serializable
    job = Job.objects.get(id=job_id)
    script = job.script_contents.read()
    input_image = Image.open(io.BytesIO(job.input_image.read()))
    kwargs = job.other_inputs or {}

    # TODO: sandbox this
    module = imp.new_module('main')
    exec(script, module.__dict__)
    output_array = module.main(input_image=input_image, **kwargs)

    storage_client = job.input_image.storage.client
    bucket_name = job.input_image.storage.bucket_name

    def store_image(image, output_index):
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        object_name = str(job.id) + '_output_' + str(output_index) + '.png'
        storage_client.put_object(
            bucket_name,
            object_name,
            data=ImageStorageBuffer(image_bytes),
            length=image_bytes.getbuffer().nbytes,
            content_type="image/*",
        )
        return f'/{bucket_name}/{object_name}'

    job.outputs = [
        output if not isinstance(output, Image.Image) else store_image(output, index)
        for index, output in enumerate(output_array)
    ]
    job.last_run = timezone.now()
    job.save()
    print(job.outputs)
