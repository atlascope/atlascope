from django.contrib import admin
from django.contrib.gis.db import models as geo_models
from django.db import models
from rest_framework import serializers

from atlascope.core.models.dataset import Dataset

NUCLEUS_ATTRIBUTES = [
    'Nucleus.Gradient.Canny.Mean',
    'Nucleus.Gradient.Canny.Sum',
    'Nucleus.Gradient.Mag.HistEnergy',
    'Nucleus.Gradient.Mag.HistEntropy',
    'Nucleus.Gradient.Mag.Kurtosis',
    'Nucleus.Gradient.Mag.Mean',
    'Nucleus.Gradient.Mag.Skewness',
    'Nucleus.Gradient.Mag.Std',
    'Nucleus.Haralick.ASM.Mean',
    'Nucleus.Haralick.ASM.Range',
    'Nucleus.Haralick.Contrast.Mean',
    'Nucleus.Haralick.Contrast.Range',
    'Nucleus.Haralick.Correlation.Mean',
    'Nucleus.Haralick.Correlation.Range',
    'Nucleus.Haralick.DifferenceEntropy.Mean',
    'Nucleus.Haralick.DifferenceEntropy.Range',
    'Nucleus.Haralick.DifferenceVariance.Mean',
    'Nucleus.Haralick.DifferenceVariance.Range',
    'Nucleus.Haralick.Entropy.Mean',
    'Nucleus.Haralick.Entropy.Range',
    'Nucleus.Haralick.IDM.Mean',
    'Nucleus.Haralick.IDM.Range',
    'Nucleus.Haralick.IMC1.Mean',
    'Nucleus.Haralick.IMC1.Range',
    'Nucleus.Haralick.IMC2.Mean',
    'Nucleus.Haralick.IMC2.Range',
    'Nucleus.Haralick.SumAverage.Mean',
    'Nucleus.Haralick.SumAverage.Range',
    'Nucleus.Haralick.SumEntropy.Mean',
    'Nucleus.Haralick.SumEntropy.Range',
    'Nucleus.Haralick.SumOfSquares.Mean',
    'Nucleus.Haralick.SumOfSquares.Range',
    'Nucleus.Haralick.SumVariance.Mean',
    'Nucleus.Haralick.SumVariance.Range',
    'Nucleus.Intensity.HistEnergy',
    'Nucleus.Intensity.HistEntropy',
    'Nucleus.Intensity.IQR',
    'Nucleus.Intensity.Kurtosis',
    'Nucleus.Intensity.MAD',
    'Nucleus.Intensity.Max',
    'Nucleus.Intensity.Mean',
    'Nucleus.Intensity.MeanMedianDiff',
    'Nucleus.Intensity.Median',
    'Nucleus.Intensity.Min',
    'Nucleus.Intensity.Skewness',
    'Nucleus.Intensity.Std',
    'Orientation.Orientation',
    'Shape.Circularity',
    'Shape.Eccentricity',
    'Shape.EquivalentDiameter',
    'Shape.Extent',
    'Shape.FSD1',
    'Shape.FSD2',
    'Shape.FSD3',
    'Shape.FSD4',
    'Shape.FSD5',
    'Shape.FSD6',
    'Shape.FractalDimension',
    'Shape.HuMoments1',
    'Shape.HuMoments2',
    'Shape.HuMoments3',
    'Shape.HuMoments4',
    'Shape.HuMoments5',
    'Shape.HuMoments6',
    'Shape.HuMoments7',
    'Shape.MinorMajorAxisRatio',
    'Shape.Solidity',
    'Shape.WeightedHuMoments1',
    'Shape.WeightedHuMoments2',
    'Shape.WeightedHuMoments3',
    'Shape.WeightedHuMoments4',
    'Shape.WeightedHuMoments5',
    'Shape.WeightedHuMoments6',
    'Shape.WeightedHuMoments7',
    'Size.Area',
    'Size.ConvexHullArea',
    'Size.MajorAxisLength',
    'Size.MinorAxisLength',
    'Size.Perimeter',
]


def nucleus_attribute_to_field_name(attribute: str):
    return attribute.replace('.', '_').lower().replace('nucleus_', '').replace('orientation_', '')


class DetectedNucleus(models.Model):
    detection_dataset = models.ForeignKey(
        Dataset,
        null=False,
        on_delete=models.CASCADE,
        related_name='detected_nuclei',
    )
    label_integer = models.IntegerField()
    centroid = geo_models.PointField()
    weighted_centroid = geo_models.PointField()
    bounding_box = geo_models.PolygonField()


for attribute in NUCLEUS_ATTRIBUTES:
    DetectedNucleus.add_to_class(
        nucleus_attribute_to_field_name(attribute),
        models.FloatField(),
    )


class DetectedNucleusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedNucleus
        fields = '__all__'


@admin.register(DetectedNucleus)
class DetectedNucleusAdmin(admin.ModelAdmin):
    list_display = ('id', 'detection_dataset')
