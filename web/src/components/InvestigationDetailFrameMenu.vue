<template>
  <v-menu
    v-model="showFrames"
    :close-on-content-click="false"
    offset-y
    max-height="500px"
  >
    <template
      v-slot:activator="{ on: onMenu, attrs: attrsMenu }"
    >
      <v-tooltip bottom>
        <template v-slot:activator="{ on: onTooltip, attrs: attrsTooltip }">
          <v-btn
            icon
            v-bind="{ ...attrsMenu, ...attrsTooltip }"
            v-on="{ ...onMenu, ...onTooltip }"
          >
            <v-icon>mdi-palette</v-icon>
          </v-btn>
        </template>
        <span>Edit the image style</span>
      </v-tooltip>
    </template>
    <v-card>
      <v-card-actions>
        <v-btn
          color="primary"
          text
          :disabled="!validColors"
          @click="updateFrameInfo"
        >
          Update
        </v-btn>
      </v-card-actions>
      <v-card-text class="ma-0 pa-0">
        <v-list>
          <v-list-item
            v-for="frame in frameInfo"
            :key="frame.frame"
            :value="frame"
          >
            <v-list-item-action>
              <v-switch
                v-model="frame.displayed"
              />
            </v-list-item-action>
            <v-list-item>
              <div class="frame-row ma-0 pa-0">
                <v-text-field
                  v-model="frame.color"
                  :hint="frame.name"
                  :rules="[isColorStringRule]"
                  persistent-hint
                  maxlength="6"
                />
              </div>
            </v-list-item>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-menu>
</template>

<style scoped>
  .frame-row {
    display: inline;
  }
</style>

<script lang="ts">
import {
  ref, defineComponent, onMounted, computed, watch, Ref,
} from '@vue/composition-api';
import store, { TiffFrame } from '../store';
import { isColorStringRule } from '../utilities/utiltyFunctions';

export default defineComponent({
  name: 'InvestigationDetailFrameMenu',

  setup() {
    const frameInfo: Ref<TiffFrame[]> = ref([]);
    const showFrames: Ref<boolean> = ref(false);
    const rootDataset = computed(() => store.state.rootDataset);
    const validColors = computed(
      () => frameInfo.value.every((frame: TiffFrame) => isColorStringRule(frame.color)),
    );

    function updateFrameInfo() {
      showFrames.value = false;
      store.dispatch.updateFrames(JSON.parse(JSON.stringify(frameInfo.value)));
    }

    function resetFrameInfo() {
      /* eslint-disable */
      frameInfo.value = [];
      if (!rootDataset.value || !rootDataset.value.id) {
        store.dispatch.updateFrames(frameInfo.value);
        return;
      }
      const additionalMetadata: any = store.state.datasetTileMetadata[rootDataset.value.id].additional_metadata;
      if ( additionalMetadata && additionalMetadata.frames) {
        frameInfo.value = additionalMetadata.frames.map((frame: any) => ({
          name: frame.Name || 'no name',
          frame: frame.Frame,
          displayed: true,
          color: 'ffffff',
        }));
      }
      store.dispatch.updateFrames(JSON.parse(JSON.stringify(frameInfo.value)));
      /* eslint-enable */
    }

    watch(rootDataset, () => {
      resetFrameInfo();
    });

    onMounted(() => {
      resetFrameInfo();
    });

    return {
      updateFrameInfo,
      frameInfo,
      showFrames,
      isColorStringRule,
      validColors,
    };
  },
});
</script>
