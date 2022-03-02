import io
import json
import shutil
import tifftools

from celery import shared_task
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from pathlib import Path

from atlascope.core.models import Dataset
from .utils import save_output_dataset


@shared_task
def run(job_id: str, original_dataset_id: str):
    """Return the average among all RGBA values in the input dataset image."""
    from atlascope.core.models import Job

    original_dataset = Dataset.objects.get(id=original_dataset_id)
    job = Job.objects.get(id=job_id)

    tiff_content = io.BytesIO(original_dataset.content.read())
    temp_location_prefix = Path('/', 'tmp', 'tiff_split', str(original_dataset_id))
    temp_location_prefix.mkdir(parents=True, exist_ok=True)

    # print(tifftools.read_tiff(tiff_content)['ifds'][0])
    tifftools.tiff_split(
        tiff_content,
        prefix=str(temp_location_prefix) + '/',
        subifds=True,
        overwrite=True,
    )
    for sub_file in temp_location_prefix.iterdir():
        content_stream = io.BytesIO(open(sub_file, 'rb').read())
        dump_stream = io.StringIO()
        tifftools.tiff_dump(sub_file, dest=dump_stream, json=True)
        outputs_dict = json.loads(dump_stream.getvalue())
        outputs_dict['origin'] = f'Job Spawned at {timezone.now()}'

        new_dataset = Dataset(
            name=f'{original_dataset.name} SubTIFF',
            description=f'SubTIFF for {original_dataset.name} as of {timezone.now()}',
            public=original_dataset.public,
            metadata=outputs_dict,
            dataset_type='tile_overlay',
            source_dataset=original_dataset,
        )
        new_dataset.content.save(
            f'SubTIFF.tif',
            InMemoryUploadedFile(
                content_stream,
                None,
                'file.png',
                'image/png',
                content_stream.getbuffer().nbytes,
                None,
            ),
        )
        new_dataset.save()
        job.resulting_datasets.add(new_dataset)

    shutil.rmtree(temp_location_prefix)

    job.complete = True
    job.save()
