<template>
  <div>
    <v-tooltip
      v-if="!selectionMode"
      bottom
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          icon
          v-bind="attrs"
          v-on="on"
          @click="() => store.commit.setSelectionMode(true)"
        >
          <v-icon>mdi-select</v-icon>
        </v-btn>
      </template>
      <span>Select a portion of the data</span>
    </v-tooltip>
    <div v-else>
      <v-btn
        v-if="!selection"
        color="secondary"
        @click="() => store.commit.setSelectionMode(false)"
      >
        Cancel
      </v-btn>
      <v-btn
        v-else
        color="primary"
        @click="saveSubimageDataset"
      >
        Create Subimage Dataset {{ selectionText() }}
      </v-btn>
    </div>
    <div
      v-if="saved"
      style="display: inline"
    >
      Saved!
    </div>
  </div>
</template>

<script lang="ts">
import {
  defineComponent, ref, computed,
} from '@vue/composition-api';
import store from '../store';

export default defineComponent({
  name: 'DatasetSubimageSelector',

  setup() {
    const selection = computed(() => store.state.subimageSelection);
    const selectionMode = computed(() => store.state.selectionMode);
    const saved = ref<boolean>(false);

    async function saveSubimageDataset() {
      const response = await store.dispatch.createSubimageDataset(selection.value);
      if (response) {
        store.commit.setSelectionMode(false);
        saved.value = true;
        setTimeout(() => { saved.value = false; }, 3000);
      }
    }
    function selectionText() {
      if (!selection.value) return '';
      return `(${selection.value[0]}, ${selection.value[1]}) -> (${selection.value[2]}, ${selection.value[3]})`;
    }

    return {
      selectionMode,
      selection,
      store,
      saved,
      saveSubimageDataset,
      selectionText,
    };
  },
});
</script>
