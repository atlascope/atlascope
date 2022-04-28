import { ref } from '@vue/composition-api';

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
  return {
    layer,
    getType,
    drawLayer,
    updateLayerUrl,
  };
}
