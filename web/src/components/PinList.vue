<template>
  <div>
    <v-toolbar
      color="white"
      flat
    >
      <v-checkbox
        :input-value="selectedPins.length === pins.length"
        :indeterminate="selectedPins.length > 0 && selectedPins.length < pins.length"
        @change="toggleDisplayAll"
      />
      <v-toolbar-title>
        Investigation Pins
      </v-toolbar-title>
    </v-toolbar>
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
          :disabled="pin.parent !== rootDataset.id"
        >
          <template v-slot:default="{ active }">
            <v-list-item-action>
              <v-checkbox
                :input-value="active"
                :disabled="pin.parent !== rootDataset.id"
              />
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ pinDisplayTitle(pin) }}</v-list-item-title>
              <v-list-item-subtitle v-if="pin.pin_type === 'DatasetPin'">
                {{ pin.description }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </template>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </div>
</template>

<script lang="ts">
import {
  computed, defineComponent, onMounted, Ref, ref, watch, PropType,
} from '@vue/composition-api';
import store from '../store';
import { Pin } from '../generatedTypes/AtlascopeTypes';

export default defineComponent({
  props: {
    zoomLevel: {
      type: Number as PropType<number>,
      required: false,
    },
    xCoord: {
      type: Number as PropType<number>,
      required: false,
    },
    yCoord: {
      type: Number as PropType<number>,
      required: false,
    },
  },

  setup(props) {
    const pins: Ref<Pin[]> = computed(() => store.state.currentPins);
    const rootDataset = computed(() => store.state.rootDataset);
    const selectedPins: Ref<Pin[]> = ref([]);

    function selectionChanged(pinList: Pin[]) {
      store.dispatch.updateSelectedPins(pinList);
    }

    function toggleDisplayAll() {
      if (selectedPins.value.length === pins.value.length) {
        selectedPins.value = [];
        selectionChanged(selectedPins.value);
      } else {
        selectedPins.value = pins.value;
        selectionChanged(selectedPins.value);
      }
    }

    function pinDisplayTitle(pin: Pin) {
      return (pin.pin_type === 'NotePin') ? `Note pin: ${pin.note?.substring(0, 25)}...` : `Child dataset: ${pin.child}`;
    }

    watch(rootDataset, () => {
      selectedPins.value = [];
    });

    watch([props.zoomLevel, props.xCoord, props.yCoord], () => {
      console.log('map prop changed');
    });

    onMounted(() => {
      // reset selectedPins
      store.state.selectedPins.forEach((pin: Pin) => {
        selectedPins.value.push(pin);
      });
    });

    return {
      pins,
      rootDataset,
      selectionChanged,
      selectedPins,
      pinDisplayTitle,
      toggleDisplayAll,
    };
  },
});
</script>
