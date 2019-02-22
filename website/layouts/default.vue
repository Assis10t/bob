<template>
    <div>

        <headroom-header 
            id="header"
            :links="[
                {
                    name: 'Home',
                    url: '/'
                },
                {
                    name: 'Meet the Bob',
                    url: '/'
                },
                {
                    name: 'Bob App',
                    url: '/'
                },
                {
                    name: 'About',
                    url: '/'
                },
                {
                    name: 'Contact us',
                    url: '/'
                },
            ]"
        >
        </headroom-header>

        <main>
            <div class="main-content">
                <nuxt />
            </div>
        </main>

        <abs-footer
            :links="[
                {
                    name: 'Home',
                    url: '/'
                },
                {
                    name: 'Contact us',
                    url: '/'
                },
            ]"
        ></abs-footer>

    </div>
</template>


<script>
import HeadroomHeader from '~/components/HeadroomHeader'
import AbsFooter from '~/components/AbsFooter'

export default {
    components: {
        HeadroomHeader,
        AbsFooter,
    },
    data: function () {
        return {

        }
    },
    methods: {
    },
    mounted: function () {

    }
};
</script>


<style>
    
</style>
