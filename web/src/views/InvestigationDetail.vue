<template>
    <div ref="map" class="map" />
</template>

<style scoped>
.map {
    width: 100%;
    height: 100%;
    padding: 0;
    margin: 0;
    overflow: hidden;
}
</style>

<script lang="ts">
import {
    ref, defineComponent, onMounted, PropType,
} from '@vue/composition-api';
import useGeoJS from '../utilities/useGeoJS';

export default defineComponent({
    name: 'InvestigationDetail',

    props: {
        investigation: {
            type: String as PropType<string>,
            required: true,
        },
    },

    setup(props) {
        const map = ref(null);
        const { zoom, center } = useGeoJS(map);

        onMounted(() => {
            setTimeout(() => center(-0.1704, 51.5047), 2000);
            setTimeout(() => zoom(14), 3000);
            console.log(props.investigation);
        });
        return { map };
    },
});
</script>
