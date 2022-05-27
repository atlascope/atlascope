import {
  ref, onMounted, Ref,
} from '@vue/composition-api';
import geo from 'geojs';
import useGeoJSLayer from './useGeoJSLayer';

export default function useGeoJS(element: Ref<HTMLElement | null>) {
  const map: Ref<any> = ref(null);
  const zoomLevel = ref(0);
  const xCoord = ref(0);
  const yCoord = ref(0);

  const geoEvents = geo.event;
  const geoAnnotations = geo.annotation;

  const updateCenter = () => {
    if (map.value !== null) {
      const { x, y } = map.value.center();
      xCoord.value = x;
      yCoord.value = y;
    }
  };

  const createMap = (mapParams?: object) => {
    const node = { node: element.value };
    const geojsMap = geo.map({ ...node, ...mapParams });
    map.value = geojsMap;

    zoomLevel.value = map.value.zoom();
    const mapCenter = map.value.center();
    xCoord.value = mapCenter.x;
    yCoord.value = mapCenter.y;

    /* eslint-disable */
    geojsMap.geoOn(geoEvents.zoom, (event: any) => {
      zoomLevel.value = event.zoomLevel;
    });
    /* eslint-enable */
    geojsMap.geoOn(geoEvents.pan, () => {
      updateCenter();
    });
    return geojsMap;
  };

  onMounted(() => {
    // `element.value` should always be an `HTMLElement` (not `null`)
    // by the time `onMounted` is called. However, it will be `null`
    // before that since the DOM isn't available at call time.

    // check if valid DOM element is passed.
    if (element.value !== null) {
      createMap();
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

  const createLayer = (
    layerType: string,
    layerParams: object,
    gcs?: string,
    returnObj = false,
  ): number | any => {
    const layer = map.value.createLayer(layerType, layerParams);
    if (gcs !== undefined) {
      layer.gcs(gcs);
    }
    if (returnObj) {
      return layer;
    }
    return useGeoJSLayer(layer, layerType);
  };

  const drawLayer = (layerId: number) => {
    const layerToDraw = map.value.layers().find((layer: any) => layer.id() === layerId);
    if (layerToDraw) {
      layerToDraw.draw();
    }
  };

  const updateLayerUrl = (layerId: number, newUrl: string) => {
    const updateLayer = map.value.layers().find((layer: any) => layer.id() === layerId);
    if (updateLayer && updateLayer.url) {
      updateLayer.url(newUrl);
    }
  };

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
    geoAnnotations,
    clampBoundsX,
    drawLayer,
    updateLayerUrl,
  };
}
