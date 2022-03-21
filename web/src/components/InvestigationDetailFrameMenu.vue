<template>
  <v-menu
    v-model="showFrames"
    :close-on-content-click="false"
    offset-y
    max-height="500px"
  >
    <template
      v-slot:activator="{ on, attrs }"
    >
      <v-btn
        color="blue"
        dark
        v-bind="attrs"
        v-on="on"
      >
        Frames
      </v-btn>
    </template>
    <v-card>
      <v-card-text>
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
                />
              </div>
            </v-list-item>
          </v-list-item>
        </v-list>
      </v-card-text>
      <v-card-actions>
        <v-btn
          color="primary"
          text
          @click="updateFrameInfo"
        >
          Save
        </v-btn>
      </v-card-actions>
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
import store from '../store';

export default defineComponent({
  name: 'InvestigationDetailFrameMenu',

  setup() {
    const frameInfo: Ref<any[]> = ref([]);
    const showFrames: Ref<boolean> = ref(false);
    const tileMetadata = computed(() => store.state.activeDatasetMetadata);

    function updateFrameInfo() {
      showFrames.value = false;
      store.dispatch.updateFrames(frameInfo.value);
    }

    function resetFrameInfo() {
      /* eslint-disable */
      frameInfo.value = [];
      const additionalMetadata: any = tileMetadata.value?.additional_metadata;
      if (additionalMetadata.frames) {
        frameInfo.value = additionalMetadata.frames.map((frame: any) => ({
          name: frame.Name || 'no name',
          frame: frame.Frame,
          displayed: true,
          color: '000000',
        }));
      }
      store.dispatch.updateFrames(frameInfo.value);
      /* eslint-enable */
    }

    watch(tileMetadata, () => {
      resetFrameInfo();
    }, { deep: true });

    return {
      updateFrameInfo,
      frameInfo,
      showFrames,
    };
  },
});
</script>
