"""Detect likely locations of nuclei in the image."""
import io

from celery import shared_task
import histomicstk as htk
import numpy as np
import scipy as sp
import skimage.color
import skimage.io
import skimage.measure

from atlascope.core.models import Dataset

from .utils import save_output_dataset

schema = {
    "type": "object",
    "required": [],
    "properties": {},
}


def detect_nuclei(input_image):
    # Invert image
    input_image = skimage.util.invert(input_image)

    # segment foreground
    foreground_threshold = 150
    im_fgnd_mask = sp.ndimage.binary_fill_holes(input_image < foreground_threshold)

    # run adaptive multi-scale LoG filter
    min_radius = 5
    max_radius = 15

    im_log_max, im_sigma_max = htk.filters.shape.cdog(
        input_image,
        im_fgnd_mask,
        sigma_min=min_radius * np.sqrt(2),
        sigma_max=max_radius * np.sqrt(2),
    )

    # detect and segment nuclei using local maximum clustering
    local_max_search_radius = 5

    im_nuclei_seg_mask, seeds, maxima = htk.segmentation.nuclear.max_clustering(
        im_log_max, im_fgnd_mask, local_max_search_radius
    )

    # filter out small objects
    min_nucleus_area = 80

    im_nuclei_seg_mask = htk.segmentation.label.area_open(
        im_nuclei_seg_mask, min_nucleus_area
    ).astype(int)

    # return a list of polygons outlining the identified nuclei
    # each polygon is a list of n points of the form [r, c]
    return [
        skimage.measure.find_contours(im_nuclei_seg_mask == index, 0.5)[0]
        for index in range(1, im_nuclei_seg_mask.max())
    ]


@shared_task
def run(job_id: str, original_dataset_id: str):
    from atlascope.core.models import Job

    original_dataset = Dataset.objects.get(id=original_dataset_id)
    job = Job.objects.get(id=job_id)

    try:
        input_image = skimage.io.imread(
            io.BytesIO(original_dataset.content.read()),
        )
        nuclei = detect_nuclei(input_image)

        job.resulting_datasets.add(
            save_output_dataset(
                original_dataset,
                job.investigation,
                'Detected Nuclei',
                None,
                {
                    'num_nuclei': len(nuclei),
                    'nucleus_detections': [
                        # switch coordinate order to get (x, y) format
                        [[point[1], point[0]] for point in poly_points]
                        for poly_points in nuclei
                    ],
                },
                dataset_type='nucleus_detection',
            )
        )
        job.complete = True
        job.save()
    except Exception as e:
        print('FAILURE!')
        print(e)
        job.failure = str(e)
        job.save()

    print()
    print()
