from . import average_color, brightest_n_pixels, tiff_split

available_job_types = {
    module.__name__.replace(f"{module.__package__}.", ''): module.run
    for module in [
        average_color,
        brightest_n_pixels,
        tiff_split,
    ]
}
