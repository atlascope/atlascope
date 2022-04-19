<template>
  <v-card class="pa-3">
    <v-select
      v-model="selectedDataset"
      label="Select data for analysis"
      :items="currentDatasets"
      item-text="name"
      clearable
    />
    <span v-if="selectedDataset && !jobSpawned">
      Please note that custom channel coloration is not used in image analysis.
    </span>
    <div
      v-if="selectedDataset && !jobSpawned"
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
    <div v-if="selectedDataset && !jobSpawned">
      <v-select
        v-model="selectedJobType"
        label="Available Job Types"
        :items="store.state.jobTypes"
      >
        <template v-slot:selection="{ item }">
          {{ item.name.replace(/_/g, ' ') }}
        </template>
        <template v-slot:item="{ item, attrs, on }">
          <v-list-item
            v-bind="attrs"
            v-on="on"
          >
            <v-list-item-content>
              <v-list-item-title>
                {{ item.name.replace(/_/g, ' ') }}
                <div class="job-type-description">
                  {{ item.description }}
                </div>
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-select>
      <div v-if="selectedJobType">
        <v-form v-model="inputFormValid">
          <v-jsonschema-form
            :schema="jobInputsSchema(selectedJobType.additional_inputs)"
            :model="jobInputs"
            :options="schemaOptions"
          />
        </v-form>
        <v-btn
          v-if="inputFormValid"
          color="primary"
          @click="spawnJob"
        >
          Spawn Job
        </v-btn>
      </div>
    </div>
    <div v-if="jobSpawned">
      Job spawned successfully! Results will appear as a Pin when the job run is complete.
    </div>
  </v-card>
</template>

<style scoped>
.job-type-description {
  color: gray;
}
</style>

<script>
import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import Draggable from 'vuedraggable';
import VJsonschemaForm from '@koumoul/vuetify-jsonschema-form';
import '@koumoul/vuetify-jsonschema-form/dist/main.css';
import { Sketch } from 'vue-color';
import {
  defineComponent, computed, ref, watch,
} from '@vue/composition-api';
import store from '../store';

Vue.use(Vuetify);

Vue.component('draggable', Draggable);
Vue.component('color-picker', Sketch);

export default defineComponent({
  components: {
    VJsonschemaForm,
  },

  setup() {
    const currentDatasets = computed(() => store.state.currentDatasets);
    const selectedDataset = ref();
    const entireImage = ref(true);
    const selection = computed(() => store.state.subimageSelection);
    const selectionMode = computed(() => store.state.selectionMode);
    const savedNotification = ref('');
    const selectedJobType = ref();
    const inputFormValid = ref(true);
    const jobInputs = ref({});
    const jobSpawned = ref(false);
    const resultPoll = ref();

    store.dispatch.fetchJobTypes();

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
        selectedDataset.value = response.name;
        savedNotification.value = response ? 'Saved!' : 'Failed to Crop.';
      } catch (e) {
        savedNotification.value = 'Failed to Crop.';
      }
      store.commit.setSelectionMode(false);
      setTimeout(() => { savedNotification.value = ''; }, 3000);
    }

    function jobInputsSchema(inputSpecs) {
      const inputSchema = {
        type: 'object',
        title: '',
        required: [],
        properties: {},
      };
      const typeMapping = {
        int: 'integer',
      };
      inputSpecs.forEach(
        (inputSpec) => {
          if (inputSpec.required) inputSchema.required.push(inputSpec.name);
          inputSchema.properties[inputSpec.name] = {
            title: inputSpec.name.toUpperCase(),
            type: typeMapping[inputSpec.class],
          };
        },
      );
      return JSON.parse(JSON.stringify(inputSchema));
    }

    const schemaOptions = {
      debug: false,
      disableAll: false,
      autoFoldObjects: true,
    };

    async function pollForPinResult(jobId) {
      if (store.state.axiosInstance) {
        const response = (await store.state.axiosInstance.get(`/jobs/${jobId}`)).data;
        if (response.complete) {
          await store.dispatch.fetchInvestigationPins();
          clearInterval(resultPoll.value);
        }
      }
    }

    async function spawnJob() {
      if (store.state.axiosInstance) {
        const response = (await store.state.axiosInstance.post('/jobs', {
          investigation: store.state.currentInvestigation.id,
          /* eslint-disable */
          original_dataset: store.state.rootDataset.id,
          job_type: selectedJobType.value.name,
          additional_inputs: jobInputs.value,
          /* eslint-enable */
        })).data;
        if (response) {
          jobSpawned.value = true;
          setTimeout(() => { jobSpawned.value = false; }, 5000);
          resultPoll.value = setInterval(() => pollForPinResult(response.id), 5000);
        }
      }
    }

    return {
      currentDatasets,
      selectedDataset,
      selectedJobType,
      entireImage,
      selection,
      selectionMode,
      savedNotification,
      store,
      schemaOptions,
      inputFormValid,
      jobInputs,
      jobSpawned,
      jobInputsSchema,
      useSelection,
      spawnJob,
    };
  },
});
</script>
