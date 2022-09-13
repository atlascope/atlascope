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
  const annotations = () => {
    if (typeof layer.value.annotations === 'function') {
      return layer.value.annotations();
    }
    return undefined;
  };
  const removeAnnotation = (annotation: any) => {
    if (typeof layer.value.removeAnnotations === 'function') {
      layer.value.removeAnnotation(annotation);
    }
  };
  const removeAllAnnotations = () => {
    if (typeof layer.value.removeAllAnnotations === 'function') {
      layer.value.removeAllAnnotations();
    }
  };
  const addGeoEventHandler = (event: any, handler: Function) => {
    if (typeof layer.value.geoOn === 'function') {
      layer.value.geoOn(event, handler);
    }
  };
  const mode = (newMode: string | null): string | null => {
    if (typeof layer.value.mode === 'function') {
      layer.value.mode(newMode);
      return layer.value.mode();
    }
    return null;
  };
  const createFeature = (featureType: string, opts?: any): any => {
    if (!['feature', 'annotation'].includes(type.value)) {
      return undefined;
    }
    const newFeature = layer.value.createFeature(featureType, opts);
    return useGeoJSFeature(newFeature, featureType);
  };
  const clearFeatures = () => {
    layer.value.features([]);
  };
  return {
    layer,
    getType,
    drawLayer,
    updateLayerUrl,
    createFeature,
    annotations,
    removeAnnotation,
    removeAllAnnotations,
    addGeoEventHandler,
    mode,
    clearFeatures,
  };
}
