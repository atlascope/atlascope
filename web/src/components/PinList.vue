<template>
  <v-list
    dense
    flat
    class="pa-0 ma-0"
  >
    <v-list-item
      v-for="pin in pins"
      :key="pin.id"
    >
      <v-list-item-icon>
        <v-icon :color="pin.color">
          mdi-circle
        </v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        {{ pin.id }}
        <v-spacer />
      </v-list-item-content>
      <v-list-item-icon>
        <v-icon @click="selectPin(pin)">
          mdi-map-marker-radius
        </v-icon>
      </v-list-item-icon>
      <v-list-item-icon>
        <v-icon>
          mdi-cog
        </v-icon>
      </v-list-item-icon>
    </v-list-item>
  </v-list>
</template>

<script lang="ts">
import { computed, defineComponent } from '@vue/composition-api';
import store from '../store';

export default defineComponent({
  setup(props, context) {
    const pins = computed(() => store.getters.pins);

    function selectPin(pin) {
      console.log(pin);
      store.commit.setLastSelectedPin(pin);
    };
    return { pins, selectPin };
  },
});
</script>
