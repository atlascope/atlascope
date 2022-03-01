<template>
  <v-sheet
    max-width="33vw"
    min-width="33vw"
  >
    <v-tabs
      centered
      grow
    >
      <v-tab>
        Pins
      </v-tab>
      <v-tab-item>
        <pin-list />
      </v-tab-item>
      <v-tab>
        Metadata
      </v-tab>
      <v-tab-item>
        <div class="ma-2 pa-2">
          <span class="metadata">
            {{ investigationMetadata }}
          </span>
        </div>
      </v-tab-item>
    </v-tabs>
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
import PinList from './PinList.vue';

export default defineComponent({
  components: {
    PinList,
  },

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
