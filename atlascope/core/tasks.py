import imp
import io
from PIL import Image
from celery import shared_task

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from atlascope.core.models import JobRun, JobRunOutputImage


@shared_task
def spawn_job(job_run_id):
    # celery arguments must be serializable
    job_run = JobRun.objects.get(id=job_run_id)
    script = job_run.script.script_contents.read()
    input_image = Image.open(io.BytesIO(job_run.input_image.read()))
    kwargs = job_run.other_inputs or {}

    # TODO: sandbox this
    module = imp.new_module('main')
    exec(script, module.__dict__)
    output_array = module.main(input_image=input_image, **kwargs)

    def store_image(image, output_index):
        filename = f'{job_run_id}_image_output_{output_index}.png'
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

        image_output_obj = JobRunOutputImage(job_run=job_run)
        image_output_obj.stored_image.save(filename, image_file)
        image_output_obj.save()

    job_run.outputs = list(
        filter(
            None,
            [
                output if not isinstance(output, Image.Image) else store_image(output, index)
                for index, output in enumerate(output_array)
            ],
        )
    )
    job_run.last_run = timezone.now()
    job_run.save()
