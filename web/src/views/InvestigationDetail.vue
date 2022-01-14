<template>
  <v-container
    class="grey lighten-3 pa-0 ma-0"
    fluid
    fill-height
  >
    <v-row class="ma-0 pa-0">
      <v-col class="ma-0 pa-0">
        <v-sheet height="90vh">
          <div
            ref="map"
            class="map"
          />
        </v-sheet>
      </v-col>
      <v-col
        cols="auto"
        class="ma-0 pa-0"
      >
        <v-sheet
          height="90vh"
          color="teal"
        >
          <v-btn
            icon
            @click.stop="toggleSidebar"
          >
            <v-icon v-if="sidebarCollapsed">
              mdi-chevron-left
            </v-icon>
            <v-icon v-else>
              mdi-chevron-right
            </v-icon>
          </v-btn>
          <investigation-sidebar v-if="!sidebarCollapsed" />
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.map {
    width: 100%;
    height: 100%;
    padding: 0;
    margin: 0;
}
</style>

<script lang="ts">
import {
  ref, defineComponent, onMounted, PropType,
} from '@vue/composition-api';
import useGeoJS from '../utilities/useGeoJS';
import store from '../store';
import InvestigationSidebar from '../components/InvestigationSidebar.vue';

export default defineComponent({
  name: 'InvestigationDetail',

  components: {
    InvestigationSidebar,
  },

  props: {
    investigation: {
      type: String as PropType<string>,
      required: true,
    },
  },

  setup(props) {
    const map = ref(null);
    const sidebarCollapsed = ref(true);
    const { zoom, center } = useGeoJS(map);
    const datasets = ['Dataset 1', 'Dataset 2', 'Dataset 3'];
    const mainViews = ['context', 'connections'];

    function toggleSidebar() {
      sidebarCollapsed.value = !sidebarCollapsed.value;
    }

    onMounted(async () => {
      setTimeout(() => center(-0.1704, 51.5047), 2000);
      setTimeout(() => zoom(14), 3000);
      await store.dispatch.fetchCurrentInvestigation(props.investigation);
    });
    return {
      map, datasets, mainViews, sidebarCollapsed, toggleSidebar,
    };
  },
});
</script>
