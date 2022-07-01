<template>
<v-data-table
  v-model="selected"
  :headers="headers"
  :items="tours"
  :expanded.sync="expanded"
  show-select
  single-select
  show-expand
  item-key="id"
>
 <template
      v-slot:expanded-item="{ headers, item }"
    >
      <td :colspan="headers.length" class="white" >
         <v-data-table
          v-model="selectedWaypoint"
          :headers="waypointHeaders"
          :items="item.waypoints"
          show-select
          single-select
          hide-default-footer
          item-key="id"
        />
      </td>
  </template>

</v-data-table>

</template>

<script lang="ts">
import { defineComponent, Ref, computed, ref} from '@vue/composition-api';
import type { DataTableHeader } from 'vuetify';

import { Tour, Waypoint } from '@/generatedTypes/AtlascopeTypes';
import store from '@/store';

export default defineComponent({
  setup() {
    const tours: Ref<Tour[]> = computed(() => store.state.tours);
    const selected:Ref<Tour[]> = computed({
      get: () => store.state.selectedTour,
      set: (val) => store.commit.setSelectedTour(val),
    })
    const selectedWaypoint: Ref<Waypoint[]> = computed({
      get: () => store.state.selectedWaypoint,
      set: (val) => store.commit.setSelectedWaypoint(val),
    })
    const expanded: Tour[] = [];


    const headers: DataTableHeader[] = [
      { text: '', value: 'data-table-select' },
      { text: 'Tour Name', value: 'name' },
      { text: '', value: 'data-table-expand' },
    ];

    const waypointHeaders: DataTableHeader[] = [
      { text: '', value: 'data-table-select' },
      { text: 'Waypoint Location', value: 'location' },
      { text: 'Zoom Level', value: 'zoom' },
    ];

    // const zoomTo = (input: {item:Waypoint, value:boolean}) => {
    //   console.log(input.value)
    //   console.log(input.item.location)
    //   if(input.value){
    //     store.commit.setSelectedWaypoint(input.item);
    //   }
    // }

    return {
      tours,
      selected,
      selectedWaypoint,
      headers,
      waypointHeaders,
      expanded,
    };
  },
});
</script>
