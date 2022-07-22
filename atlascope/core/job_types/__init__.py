from . import average_color, brightest_n_pixels, gland_detection, nucleus_detection

available_job_types = {
    module.__name__.replace(f"{module.__package__}.", ''): module
    for module in [
        average_color,
        brightest_n_pixels,
        gland_detection,
        nucleus_detection,
    ]
}
