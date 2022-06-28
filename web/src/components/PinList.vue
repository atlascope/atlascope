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
          v-for="pin in sortedPins"
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
            <v-list-item-action>
              <v-tooltip right>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    icon
                    v-bind="attrs"
                    v-on="on"
                    @click.prevent.stop="togglePin(pin)"
                  >
                    <v-icon>mdi-eye</v-icon>
                  </v-btn>
                </template>
                <span>Show this pin's data on the map</span>
              </v-tooltip>
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
  computed, defineComponent, onMounted, Ref, ref, watch, inject,
} from '@vue/composition-api';
import store from '../store';
import { Pin } from '../generatedTypes/AtlascopeTypes';
import { Point, postGisToPoint } from '../utilities/utiltyFunctions';

export default defineComponent({
  setup() {
    const pins: Ref<Pin[]> = computed(() => store.state.currentPins);
    const bounds = computed(() => store.state.currentBounds);
    const zoom = computed(() => store.state.zoomLevel);
    const rootDataset = computed(() => store.state.rootDataset);

    function isInBounds(pin: Pin): boolean {
      const point: Point = postGisToPoint(pin.location) || { x: 0, y: 0 };
      const containedInMapBounds = (point.x < bounds.value.right
        && point.x > bounds.value.left
        && point.y > bounds.value.top
        && point.y < bounds.value.bottom);
      const pinMaxZoom = pin.maximum_zoom || 40;
      const pinMinZoom = pin.minimum_zoom || 0;
      const visibleAtCurrentZoom = (
        pinMinZoom - 2 <= zoom.value
        && pinMaxZoom + 2 >= zoom.value
      );
      return containedInMapBounds && visibleAtCurrentZoom;
    }

    const sortedPins = computed(() => store.state.currentPins.slice().sort(
      (firstPin, secondPin) => {
        const firstPinInBounds = isInBounds(firstPin);
        const secondPinInBounds = isInBounds(secondPin);
        if (firstPinInBounds && secondPinInBounds) {
          return firstPin.id - secondPin.id;
        }
        return firstPinInBounds ? -1 : 1;
      },
    ));
    const selectedPins: Ref<Pin[]> = ref([]);
    const togglePin = inject<Function>('togglePin');

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
      sortedPins,
      togglePin,
    };
  },
});
</script>
