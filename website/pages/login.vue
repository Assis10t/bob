<template>
    <section class="is-medium is-full-height">
        <div class="container is-flex justify-center align-center is-full-height">
            <div class="box">
                <form action="">
                    <div class="field">
                        <label class="label">Email:</label>
                        <div class="control">
                            <input class="input" type="email" v-model="email" placeholder="Enter your email">
                        </div>
                        <!-- <p class="help">This is a help text</p> -->
                    </div>
                    <div class="field">
                        <label class="label">Password:</label>
                        <div class="control">
                            <input class="input" type="password" v-model="password" placeholder="Enter your password">
                        </div>
                        <!-- <p class="help">This is a help text</p> -->
                    </div>
                    <div class="field">
                        <div class="control">
                            <input type="submit" class="button is-link" value="Login"  @click.stop.prevent="login()">
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </section>
</template>

<script>
import firebase, {auth} from '~/services/fireinit'

export default {
    data: function () {
        return {
            email: null,
            password: null
        }
    },
    methods: {
        login () {
            // this.$store.dispatch('logIn').then(() => {
            //     location.reload()
            // }).catch((e) => {
            //     console.log(e.message)
            // })

            firebase.auth().signInWithEmailAndPassword(this.email, this.password)
                .then((res) => {
                    console.log(res)
                    this.$store.commit('setUser', res.user)
                })
                .catch(function(error) {
                var errorCode = error.code;
                var errorMessage = error.message;
                console.log(error.code)
                console.log(error.message)
            });

            console.log(this.$store.state.user)
        }
    }
};
</script>

<style lang="sass" scoped>

    .box
        width: 32rem    

</style>
