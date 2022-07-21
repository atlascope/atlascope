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

import vtkActor from '@kitware/vtk.js/Rendering/Core/Actor';
import vtkMapper from '@kitware/vtk.js/Rendering/Core/Mapper';
import vtkConeSource from '@kitware/vtk.js/Filters/Sources/ConeSource';

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
        const renderer = genericRenderer.getRenderer();
        const renderWindow = genericRenderer.getRenderWindow();
        const coneSource = vtkConeSource.newInstance({ height: 1.0 });

        const mapper = vtkMapper.newInstance();
        mapper.setInputConnection(coneSource.getOutputPort());

        const actor = vtkActor.newInstance();
        actor.setMapper(mapper);

        renderer.addActor(actor);
        renderer.resetCamera();
        renderWindow.render();

        context.value = {
          genericRenderer,
          renderWindow,
          renderer,
          coneSource,
          actor,
          mapper,
        };
      }
    });

    onBeforeUnmount(() => {
      if (context.value) {
        const {
          genericRenderer,
          coneSource,
          actor,
          mapper,
        } = context.value;
        actor.delete();
        mapper.delete();
        coneSource.delete();
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
  height: 40%;
  width: 100%;
}

.vtkcontainer {
  height: 100%;
}
</style>
