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
    // should always be HTMLElement in onMounted if passed a valid div
    // TODO: handle case when passed invalid div
    if (element.value !== null) {
      map.value = geo.map({ node: element.value });
      map.value.createLayer('osm');
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
}
