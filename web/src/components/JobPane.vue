<template>
  <v-card class="pa-3">
    <v-select
      v-model="selectedDataset"
      label="Select data for analysis"
      :items="currentDatasets"
      item-text="name"
      clearable
    />
    <div
      v-if="selectedDataset"
      style="display:flex; justify-content:space-between"
    >
      <v-switch
        v-model="entireImage"
        label="Analyze entire image"
      />
      <div
        v-if="savedNotification && !entireImage"
        style="display: inline"
      >
        {{ savedNotification }}
      </div>
      <v-btn
        v-if="!selectionMode && !entireImage"
        @click="() => store.commit.setSelectionMode(true)"
      >
        Select Region
      </v-btn>
      <v-btn
        v-if="selection && !entireImage"
        color="primary"
        @click="useSelection"
      >
        Use Selection
      </v-btn>
      <v-btn
        v-if="selectionMode && !entireImage"
        color="secondary"
        @click="() => store.commit.setSelectionMode(false)"
      >
        Cancel
      </v-btn>
    </div>
  </v-card>
</template>

<script>
import {
  defineComponent, computed, ref, watch,
} from '@vue/composition-api';
import store from '../store';

export default defineComponent({

  setup() {
    const currentDatasets = computed(() => store.state.currentDatasets);
    const selectedDataset = ref();
    const entireImage = ref(true);
    const selection = computed(() => store.state.subimageSelection);
    const selectionMode = computed(() => store.state.selectionMode);
    const savedNotification = ref('');

    watch(selectedDataset, () => {
      if (selectedDataset.value) {
        store.commit.setRootDataset(
          currentDatasets.value.find(
            (dataset) => dataset.name === selectedDataset.value,
          ),
        );
        store.commit.setShowEmbeddings(false);
      } else {
        store.commit.resetRootDataset();
        store.commit.setShowEmbeddings(true);
      }
    });

    async function useSelection() {
      try {
        const response = await store.dispatch.createSubimageDataset(selection.value);
        store.commit.setCurrentDatasets(store.state.currentDatasets.concat([response]));
        selectedDataset.value = response;
        savedNotification.value = response ? 'Saved!' : 'Failed to Crop.';
      } catch (e) {
        savedNotification.value = 'Failed to Crop.';
      }
      store.commit.setSelectionMode(false);
      setTimeout(() => { savedNotification.value = ''; }, 3000);
    }

    return {
      currentDatasets,
      selectedDataset,
      entireImage,
      selection,
      selectionMode,
      savedNotification,
      store,
      useSelection,
    };
  },
});
</script>
