import { Dataset } from '@/generatedTypes/AtlascopeTypes';
import { GeoJSLayer, GeoJSFeature } from './composableTypes';

function visualizeAvgColor(
  data: Dataset,
  featureLayer: GeoJSLayer,
) {
  const grid: GeoJSFeature = featureLayer.createFeature('grid', {
    grid: {
      gridWidth: 8,
      gridHeight: 7,
      x0: 0,
      y0: 0,
      dx: 0.1,
      dy: 0.08,
      stepped: false,
    },
  });
  grid.data([
    0, 1, 2, 3, 2, 1, 0,
    1, 2, 3, 4, 3, 2, 1,
    2, 3, 4, 5, 4, 3, 2,
    3, 4, 5, 6, 5, 4, 3,
    2, 3, 4, 5, 6, 5, 4,
    1, 2, 3, 4, 5, 6, 5,
  ]);
  grid.draw();
  console.log(grid);
  console.log(featureLayer.layer.value.features());
  const features = featureLayer.layer.value.features();
  console.log(features.map((feature) => feature.data()));
}

export default function visualize(
  data: Dataset,
  featureLayer: GeoJSLayer | undefined,
) {
  if (!featureLayer) {
    return;
  }
  if (data.dataset_type === 'average_color') {
    visualizeAvgColor(data, featureLayer);
  }
}
