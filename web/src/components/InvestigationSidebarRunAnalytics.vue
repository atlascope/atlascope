<template>
  <div class="ma-2 pa-2">
    <v-select
      v-if="jobs.length > 0"
      v-model="selectedJob"
      label="Select a job to run"
      :items="jobs"
      item-text="name"
      item-value="id"
      return-object
    />
    <!-- For now, just use a big text field and show expected inputs -->
    <span
      v-if="selectedJobInputs"
      class="show-white-space"
    >
      {{ selectedJobInputs }}
    </span>
    <v-textarea
      v-if="selectedJob"
      label="Input Values"
    />
    <v-btn
      v-if="selectedJob"
    >
      Submit
    </v-btn>
  </div>
</template>

<style scoped>
.show-white-space {
  white-space: pre;
}
</style>

<script lang="ts">
import {
  computed, defineComponent, ref, Ref,
} from '@vue/composition-api';
import store from '../store';

export default defineComponent({
  setup() {
    const jobs = computed(() => store.getters.jobs);
    const selectedJob: Ref<any | null> = ref(null);
    const selectedJobInputs: Ref<string> = computed(() => {
      if (!selectedJob.value || !selectedJob.value.inputs) {
        return '';
      }
      return JSON.stringify(selectedJob.value.inputs, undefined, 4);
    });
    return { jobs, selectedJob, selectedJobInputs };
  },
});
</script>
