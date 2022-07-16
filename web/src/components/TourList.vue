<template>
  <v-data-table
    v-model="expanded"
    :headers="headers"
    :items="tours"
    :expanded.sync="expanded"
    single-expand
    show-expand
    item-key="id"
  >
    <template v-slot:expanded-item="{ headers, item }">
      <td
        :colspan="headers.length"
        class="white"
      >
        <v-stepper
          v-model="currentStep"
          vertical
        >
          <template>
            <div class="d-flex justify-space-between mx-5">
              <v-btn
                color="primary"
                :disabled="currentStep == 0 || currentStep == 1"
                @click="previousStep()"
              >
                Previous
              </v-btn>
              <v-btn
                color="primary"
                :disabled="currentStep == item.waypoints.length"
                @click="nextStep()"
              >
                Next
              </v-btn>
            </div>
          </template>
          <template v-for="n in item.waypoints.length">
            <v-stepper-step
              :key="`${n}-item.waypoints.id`"
              :step="n"
              editable
            >
              Waypoint Location: {{ item.waypoints[n - 1].location.split(";")[1] }}
            </v-stepper-step>
          </template>
        </v-stepper>
      </td>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import {
  defineComponent, Ref, computed, ref, watch,
} from '@vue/composition-api';
import type { DataTableHeader } from 'vuetify';

import { Tour, Waypoint } from '@/generatedTypes/AtlascopeTypes';
import store from '@/store';

export default defineComponent({
  setup() {
    const tours: Ref<Tour[]> = computed(() => store.state.tours);
    const expanded: Ref<Tour[]> = computed({
      get: () => store.state.selectedTour,
      set: (val) => store.commit.setSelectedTour(val),
    });
    const selectedWaypoint: Ref<Waypoint> = computed({
      get: () => store.state.selectedWaypoint,
      set: (val) => store.commit.setSelectedWaypoint(val),
    });

    const headers: DataTableHeader[] = [
      { text: 'Tour Name', value: 'name' },
      { text: '', value: 'data-table-expand' },
    ];

    const currentStep = ref<number>(0);

    const nextStep = () => {
      currentStep.value += 1;
    };

    const previousStep = () => {
      currentStep.value -= 1;
    };

    watch(currentStep, () => {
      selectedWaypoint.value = tours.value[
        tours.value.indexOf(expanded.value[0])
      ].waypoints[currentStep.value - 1];
    });

    return {
      tours,
      selectedWaypoint,
      headers,
      expanded,
      currentStep,
      nextStep,
      previousStep,
    };
  },
});
</script>
