<template>
  <v-list
    dense
    flat
    class="pa-0 ma-0"
  >
    <v-list-item-group>
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
        </v-list-item-content>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script lang="ts">
import { computed, defineComponent } from '@vue/composition-api';
import store from '../store';

export default defineComponent({
  setup() {
    const pins = computed(() => store.getters.pins);
    return { pins };
  },
});
</script>
