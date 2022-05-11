<template>
  <div>
    <v-tooltip bottom>
      <template v-slot:activator="{ on: onTooltip, attrs: attrsTooltip }">
        <v-btn
          icon
          v-bind="attrsTooltip"
          v-on="onTooltip"
          @click="showFrames = !showFrames"
        >
          <v-icon>mdi-palette</v-icon>
        </v-btn>
      </template>
      <span>Edit the image style</span>
    </v-tooltip>
    <v-dialog
      v-model="showFrames"
      max-width="400px"
      persistent
    >
      <v-card>
        <v-card-actions>
          <v-btn
            color="primary"
            text
            @click="updateFrameInfo"
          >
            Update
          </v-btn>
          <v-spacer />
          <v-btn
            color="error"
            text
            @click="cancelChanges"
          >
            Cancel
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
                    persistent-hint
                    maxlength="6"
                    readonly
                  >
                    <template v-slot:prepend>
                      <v-menu
                        v-model="frame.menu"
                        :close-on-content-click="false"
                      >
                        <template v-slot:activator="{ on: onSwatch }">
                          <div
                            :style="{ 'backgroundColor': frame.color }"
                            class="swatch"
                            v-on="onSwatch"
                          />
                        </template>
                        <v-card>
                          <v-card-text class="pa-0">
                            <v-color-picker
                              v-model="frame.color"
                              mode="hexa"
                              hide-mode-switch
                            />
                          </v-card-text>
                        </v-card>
                      </v-menu>
                    </template>
                  </v-text-field>
                </div>
              </v-list-item>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
  .frame-row {
    display: inline;
  }

  .swatch {
    border: 1px solid black;
    border-radius: 4px;
    margin-bottom: 1px;
    height: 30px;
    width: 30px;
    cursor: pointer;
  }
</style>

<script lang="ts">
import {
  ref, defineComponent, onMounted, computed, watch, Ref,
} from '@vue/composition-api';
import store, { TiffFrame } from '../store';

export default defineComponent({
  name: 'InvestigationDetailFrameMenu',

  setup() {
    const frameInfo: Ref<TiffFrame[]> = ref([]);
    const showFrames: Ref<boolean> = ref(false);
    const rootDataset = computed(() => store.state.rootDataset);

    function updateFrameInfo() {
      showFrames.value = false;
      store.dispatch.updateFrames(JSON.parse(JSON.stringify(frameInfo.value)));
    }

    function cancelChanges() {
      showFrames.value = false;
      frameInfo.value = JSON.parse(JSON.stringify(store.state.rootDatasetFrames));
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
          color: '#FFFFFF',
          menu: false,
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
      cancelChanges,
      frameInfo,
      showFrames,
    };
  },
});
</script>
