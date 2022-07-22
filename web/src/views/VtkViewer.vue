<template>
  <div
    ref="viewerContainer"
    class="viewercontainer"
  >
    <div
      ref="vtkContainer"
      class="vtkcontainer"
    />
    <table class="controls">
      <tbody>
        <tr>
          <td>
            <select
              style="width: 100%"
              :value="representation"
              @change="setRepresentation($event.target.value)"
            >
              <option value="0">
                Points
              </option>
              <option value="1">
                Wireframe
              </option>
              <option value="2">
                Surface
              </option>
            </select>
          </td>
        </tr>
        <tr>
          <td>
            <input
              type="range"
              min="4"
              max="80"
              :value="coneResolution"
              @input="setConeResolution($event.target.value)"
            >
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import {
  ref, unref, onMounted, onBeforeUnmount, watchEffect,
} from '@vue/composition-api';

import '@kitware/vtk.js/Rendering/Profiles/Geometry';

import vtkRenderWindow from '@kitware/vtk.js/Rendering/Misc/GenericRenderWindow';
import vtkHttpDataSetReader from '@kitware/vtk.js/IO/Core/HttpDataSetReader';
import '@kitware/vtk.js/IO/Core/DataAccessHelper/HttpDataAccessHelper';

import vtkActor from '@kitware/vtk.js/Rendering/Core/Actor';
import vtkMapper from '@kitware/vtk.js/Rendering/Core/Mapper';

export default {
  name: 'VtkViewer',

  setup() {
    const vtkContainer = ref(null);
    const viewerContainer = ref(null);
    const context = ref(null);
    const coneResolution = ref(6);
    const representation = ref(2);

    function setConeResolution(res) {
      coneResolution.value = Number(res);
    }

    function setRepresentation(rep) {
      representation.value = Number(rep);
    }

    watchEffect(() => {
      const res = unref(coneResolution);
      const rep = unref(representation);
      if (context.value) {
        const { actor, coneSource, renderWindow } = context.value;
        coneSource.setResolution(res);
        actor.getProperty().setRepresentation(rep);
        renderWindow.render();
      }
    });

    onMounted(() => {
      if (!context.value) {
        const genericRenderer = vtkRenderWindow.newInstance();
        genericRenderer.setContainer(vtkContainer.value);
        genericRenderer.resize();

        const reader = vtkHttpDataSetReader.newInstance({ fetchGzip: true });

        const renderer = genericRenderer.getRenderer();
        const renderWindow = genericRenderer.getRenderWindow();

        const mapper = vtkMapper.newInstance();
        mapper.setInputConnection(reader.getOutputPort());

        const actor = vtkActor.newInstance();
        actor.setMapper(mapper);

        reader.setUrl('https://kitware.github.io/vtk-js/data/cow.vtp')
          .then(() => reader.loadData())
          .then(() => {
            renderer.addVolume(actor);
            renderer.resetCamera();
            renderWindow.render();
          });

        context.value = {
          genericRenderer,
          renderWindow,
          renderer,
          reader,
          actor,
          mapper,
        };
      }
    });

    onBeforeUnmount(() => {
      if (context.value) {
        const {
          genericRenderer,
          reader,
          actor,
          mapper,
        } = context.value;
        actor.delete();
        mapper.delete();
        reader.delete();
        genericRenderer.delete();
        context.value = null;
      }
    });

    return {
      vtkContainer,
      viewerContainer,
      setRepresentation,
      setConeResolution,
      coneResolution,
      representation,
    };
  },
};
</script>

<style scoped>
.controls {
  position: absolute;
  top: 75px;
  right: 25px;
  background: white;
  padding: 12px;
}

.viewercontainer {
  height: 900px;
  width: 100%;
}

.vtkcontainer {
  height: 100%;
}
</style>
