import {
  ref, onMounted, Ref,
} from '@vue/composition-api';

import geo from 'geojs';

export default function useGeoJS(element: Ref<HTMLElement | null>) {
  const map: Ref<any> = ref(null);

  onMounted(() => {
    // should always be HTMLElement in onMounted if passed a valid div
    // TODO: handle case when passed invalid div
    if (element.value !== null) {
      map.value = geo.map({ node: element.value });
      map.value.createLayer('osm');
    }
  });
}
