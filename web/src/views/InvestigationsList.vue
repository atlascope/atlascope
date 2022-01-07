<template>
    <v-container class="pa-6" fluid>
        <v-row class="pa-6">
            <v-col v-for="investigation in investigations" :key="investigation.id" md="3">
                <v-card elevation="9"  rounded-lg outline>
                    <v-card-title>{{ investigation.name }}</v-card-title>
                    <v-card-subtitle>{{ investigation.owner }}</v-card-subtitle>
                    <v-card-text>{{ investigation.description }}</v-card-text>
                    <v-card-actions>
                        <router-link :to="`/investigations/${investigation.id}`">
                            <v-btn color="blue" text>Investigate</v-btn>
                        </router-link>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from 'vue';
import { Investigation } from '../generatedTypes/AtlascopeTypes';

export default Vue.extend({
    props: {

    },

    data() {
        return {};
    },

    computed: {
        investigations(): Array<Investigation> {
            return [
                {
                    id: '1',
                    name: 'Investigation 1',
                    description: 'Lorem ipsum ...',
                    owner: 'Alice',
                },
                {
                    id: '2',
                    name: 'Investigation 2',
                    description: 'Lorem ipsum ...',
                    owner: 'Bob',
                },
                {
                    id: '3',
                    name: 'Investigation 3',
                    description: 'Lorem ipsum ...',
                    owner: 'Carol',
                },
                {
                    id: '4',
                    name: 'Investigation 4',
                    description: 'Lorem ipsum ...',
                    owner: 'Dan',
                },
                {
                    id: '5',
                    name: 'Investigation 5',
                    description: 'Lorem ipsum ...',
                    owner: 'Eileen',
                },
                {
                    id: '6',
                    name: 'Investigation 6',
                    description: 'Lorem ipsum ...',
                    owner: 'Frank',
                },
            ];
        },
    },

    methods: {
        printSomething() {
            console.log('Clicked a card action');
        },
    },
});
</script>
