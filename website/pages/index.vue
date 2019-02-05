<template>
    <section class="hero is-medium is-primary is-bold">
        <div class="hero-body">
            <div class="container">
                <h1 class="title">
                    Meet the Bob {{ user }}
                </h1>
                <h2 class="subtitle">
                    Brilliant Online Buying
                </h2>
            </div>
        </div>
    </section>
</template>

<script>
// import Logo from "~/components/Logo.vue";

export default {
//   components: {
//     Logo
//   }
    data: function () {
        return {

        }
    },
    computed: {
        user: function () {
            return this.$store.state.user
        }
    }
};
</script>

<style lang="sass">
</style>
