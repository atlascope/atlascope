import imp
import io

from PIL import Image
from celery import shared_task
from django.apps import apps
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone


@shared_task
def spawn_job(job_run_id):
    # celery arguments must be serializable
    job_run = apps.get_model('core', 'JobRun').objects.get(id=job_run_id)
    script = job_run.script.script_contents.read()
    input_image = Image.open(io.BytesIO(job_run.input_image.read()))
    kwargs = job_run.other_inputs or {}

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
        filename = f'{job_run_id}_image_output_{output_key}.png'
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

        image_output_obj = apps.get_model('core', 'JobRunOutputImage')(job_run=job_run)
        image_output_obj.stored_image.save(filename, image_file)
        image_output_obj.save()
        return image_output_obj.stored_image.url

    job_run.outputs = {key: interpret_output(key, output) for key, output in output_dict.items()}
    job_run.last_run = timezone.now()
    job_run.save()
