import { ref } from '@vue/composition-api';
import useGeoJSFeature from './useGeoJSFeature';

export default function useGeoJSLayer(geoJSLayer: any, layerType: string) {
  const layer = ref(geoJSLayer);
  const type = ref(layerType);
  const getType = () => type.value;
  const drawLayer = () => {
    layer.value.draw();
  };
  const updateLayerUrl = (newUrl: string) => {
    if (type.value !== 'osm') {
      return;
    }
    layer.value.url(newUrl);
  };
  const createFeature = (featureType: string): any => {
    if (!['feature', 'annotation'].includes(type.value)) {
      return undefined;
    }
    const newFeature = layer.value.createFeature('point');
    return useGeoJSFeature(newFeature, featureType);
  };
  return {
    layer,
    getType,
    drawLayer,
    updateLayerUrl,
    createFeature,
  };
}
