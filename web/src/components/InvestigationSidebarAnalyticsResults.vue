<template>
  <div class="ma-2 pa-2">
    <v-select
      v-if="jobResults.length > 0"
      v-model="currentJob"
      label="View results of a job"
      :items="jobResults"
      item-value="id"
      item-text="id"
      return-object
    />
    <div v-if="currentJob">
      <!--
        Here is where we can display job results. We should consider what kind
        of data each job has created, and use the correct component. For now,
        just display a string representing the job
      -->
      <span class="show-white-space">{{ currentJobStringRep }}</span>
    </div>
  </div>
</template>

<style scoped>
.show-white-space {
  padding: 0px;
  margin: 0px;
  white-space: pre;
}

.results-image-container {
  width: 100%;
  display: grid;
  justify-content: center;
}
</style>

<script lang="ts">
import {
  computed, defineComponent, Ref, ref,
} from '@vue/composition-api';
import store from '../store';
import { Job } from '../generatedTypes/AtlascopeTypes';

export default defineComponent({
  setup() {
    const jobResults = computed(() => store.state.jobs);
    const currentJob: Ref<Job | null> = ref(null);
    const currentJobStringRep = computed(() => JSON.stringify(currentJob, undefined, 4));

    const iconType = (jobStatus: string) => {
      switch (jobStatus) {
        case 'running':
          return 'mdi-head-dots-horizontal';
        case 'error':
          return 'mdi-close';
        case 'success':
          return 'mdi-check';
        default:
          return '';
      }
    };
    return {
      jobResults,
      iconType,
      currentJob,
      currentJobStringRep,
    };
  },
});
</script>
