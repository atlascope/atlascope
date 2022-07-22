import { Dataset } from '@/generatedTypes/AtlascopeTypes';
import { GeoJSLayer, GeoJSFeature } from './composableTypes';

function visualizeAvgColor(
  data: Dataset,
  featureLayer: GeoJSLayer,
) {
  const grid: GeoJSFeature = featureLayer.createFeature('grid');
  grid.data(new Array(1000).fill(1));
  grid.draw();
  console.log(grid);
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
