import { ref } from '@vue/composition-api';
import geo from 'geojs';
import { GeoPosition, MouseClickEvent } from './composableTypes';

export default function useGeoJSFeature(geoJSFeature: any, featureType: string) {
  const feature = ref(geoJSFeature);
  const type = ref(featureType);
  const getType = () => type.value;
  const data = (newData: object[]) => {
    if (typeof feature.value.data === 'function') {
      feature.value.data(newData);
    }
  };
  const getData = () => {
    if (typeof feature.value.data === 'function') {
      return feature.value.data();
    }
    return [];
  };
  const position = (newPosition: Function | GeoPosition) => {
    if (typeof feature.value.position === 'function') {
      feature.value.position(newPosition);
    }
  };
  const style = (newStyle: object | string, newValue?: string | Function) => {
    if (typeof feature.value.style === 'function') {
      if (typeof style === 'object') {
        feature.value.style(newStyle);
      } else {
        feature.value.style(newStyle, newValue);
      }
    }
  };
  const draw = () => {
    if (typeof feature.value.draw === 'function') {
      feature.value.draw();
    }
  };
  const featureGcsToDisplay = (x: number, y: number) => {
    if (typeof feature.value.featureGcsToDisplay === 'function') {
      return feature.value.featureGcsToDisplay({ x, y });
    }
    return { x: 0, y: 0, z: 0 };
  };
  const addGeoEventHandler = (event: any, handler: Function) => {
    if (typeof feature.value.geoOn === 'function') {
      feature.value.geoOn(event, handler);
    }
  };
  return {
    feature,
    getType,
    data,
    getData,
    position,
    style,
    draw,
    featureGcsToDisplay,
    addGeoEventHandler,
  };
}
