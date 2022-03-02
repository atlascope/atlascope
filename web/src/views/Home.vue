<script lang="ts">
import {
  ref, defineComponent, inject, onMounted,
} from '@vue/composition-api';
import useGeoJS from '../utilities/useGeoJS';

export default defineComponent({
  setup() {
    const map = ref(null);

    const { zoom, center } = useGeoJS(map);

    onMounted(() => {
      setTimeout(() => center(-0.1704, 51.5047), 2000);
      setTimeout(() => zoom(14), 4000);
    });
    return { map };
  },
});
</script>

<template>
  <div
    ref="map"
    class="map"
  />
</template>

<style scoped>
.map {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  overflow: hidden;
}
</style>
