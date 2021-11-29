import { ref, onMounted, getCurrentInstance } from '@vue/composition-api';
import geo from 'geojs';

export default function useGeoJS() {
  const map = ref(null);

  onMounted(() => {
    const inst = getCurrentInstance();
    if (inst) {
      const geojsmap = geo.map({ node: inst.vnode.elm });
      geojsmap.createLayer('osm');
      map.value = geojsmap;
    }
  });
}
