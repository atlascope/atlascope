<template>
  <v-list
    three-line
    dense
    flat
    class="ma-0 pa-0"
  >
    <v-list-item-group
      v-model="selectedPins"
      multiple
      @change="selectionChanged"
    >
      <v-list-item
        v-for="pin in pins"
        :key="pin.id"
        :value="pin"
      >
        <template v-slot:default="{ active }">
          <v-list-item-action>
            <v-checkbox :input-value="active" />
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ pinDisplayTitle(pin) }}</v-list-item-title>
            <v-list-item-subtitle>{{ pin.note }}</v-list-item-subtitle>
          </v-list-item-content>
        </template>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script lang="ts">
import {
  computed, defineComponent, onMounted, Ref, ref,
} from '@vue/composition-api';
import store from '../store';
import { Pin } from '../generatedTypes/AtlascopeTypes';

export default defineComponent({
  setup() {
    const pins: Ref<Pin[]> = computed(() => store.state.currentPins);
    const selectedPins: Ref<Pin[]> = ref([]);
    function selectionChanged(pinList: Pin[]) {
      store.dispatch.updateSelectedPins(pinList);
    }

    function pinDisplayTitle(pin: Pin) {
      return (!pin.child) ? `Note pin: ${pin.note?.substring(0, 25)}...` : `Child dataset: ${pin.child}`;
    }

    onMounted(() => {
      // reset selectedPins
      store.state.selectedPins.forEach((pin) => {
        selectedPins.value.push(pin);
      });
    });

    return {
      pins,
      selectionChanged,
      selectedPins,
      pinDisplayTitle,
    };
  },
});
</script>
