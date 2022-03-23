import {
  ref, onMounted, Ref,
} from '@vue/composition-api';

import geo from 'geojs';

export default function useGeoJS(element: Ref<HTMLElement | null>) {
  const map: Ref<any> = ref(null);
  const zoomLevel = ref(0);
  const xCoord = ref(0);
  const yCoord = ref(0);

  onMounted(() => {
    // `element.value` should always be an `HTMLElement` (not `null`)
    // by the time `onMounted` is called. However, it will be `null`
    // before that since the DOM isn't available at call time.

    // check if valid DOM element is passed.
    if (element.value !== null) {
      map.value = geo.map({ node: element.value });
      zoomLevel.value = map.value.zoom();
    }
  });

  const center = (x: number, y: number) => {
    if (map.value !== null) {
      map.value.center({ x, y });
      xCoord.value = x;
      yCoord.value = y;
    }
  };

  const zoom = (level: number) => {
    if (map.value !== null) {
      map.value.zoom(level);
      zoomLevel.value = level;
    }
  };

  const clampBoundsX = (value: boolean): boolean | undefined => {
    if (map.value) {
      return map.value.clampBoundsX(value);
    }
    return undefined;
  };

  const exit = () => {
    map.value.exit();
  };

  const createMap = (mapParams?: object) => {
    const node = { node: element.value };
    map.value = geo.map({ ...node, ...mapParams });
  };

  const createLayer = (layerType: string, layerParams: object, gcs?: string) => {
    const layer = map.value.createLayer(layerType, layerParams);
    if (gcs !== undefined) {
      layer.gcs(gcs);
    }
    return layer;
  };

  const geoEvents = geo.event;

  const generatePixelCoordinateParams = (
    width: number,
    height: number,
    tileWidth: number,
    tileHeight: number,
  ) => geo.util.pixelCoordinateParams(
    element.value,
    width,
    height,
    tileWidth,
    tileHeight,
  );

  return {
    map,
    center,
    zoom,
    zoomLevel,
    xCoord,
    yCoord,
    exit,
    createMap,
    createLayer,
    generatePixelCoordinateParams,
    geoEvents,
    clampBoundsX,
  };
}
