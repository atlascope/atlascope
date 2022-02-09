<template>
  <v-expansion-panels
    accordian
    flat
  >
    <v-expansion-panel>
      <v-expansion-panel-header>
        Pins
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <pin-list />
      </v-expansion-panel-content>
    </v-expansion-panel>
    <v-expansion-panel>
      <v-expansion-panel-header>
        Metadata
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <span class="metadata">
          {{ investigationMetadata }}
        </span>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<style scoped>
.metadata {
    white-space: pre;
}
</style>

<script lang="ts">
import { defineComponent, computed } from '@vue/composition-api';
import PinList from './PinList.vue';
import store from '../store';

export default defineComponent({
  components: {
    PinList,
  },

  setup() {
    const metadataFields = [
      'id',
      'owner',
      'investigators',
      'observers',
      'created',
      'updated',
      'description',
      'notes',
    ];
    const investigationMetadata = computed(
      () => JSON.stringify(store.state.currentInvestigation, metadataFields, 4),
    );
    return { investigationMetadata };
  },
});
</script>
