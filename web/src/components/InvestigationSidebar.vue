<template>
  <v-sheet
    max-width="33vw"
    min-width="33vw"
  >
    <v-expansion-panels
      accordian
      flat
    >
      <v-expansion-panel>
        <v-expansion-panel-header>
          Pins
        </v-expansion-panel-header>
        <v-expansion-panel-content />
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
  </v-sheet>
</template>

<style scoped>
.metadata {
    white-space: pre;
}
</style>

<script lang="ts">
import {
  defineComponent, computed,
} from '@vue/composition-api';
import store from '../store';

export default defineComponent({
  setup() {
    const metadataFields = [
      'id',
      'owner',
      'investigators',
      'ovservers',
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
