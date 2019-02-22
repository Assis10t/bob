<template>
    <div>
        <page-title
            title="Register your account"
            desc="You can register as a merchant if you are in possession of a Bob robot. If you are a customer, please download our App."
        ></page-title>

        <section class="section">
            <div class="container is-flex justify-center">
                <div class="box third-width p30 pl50 pr50">
                    <form action="">
                        <div class="field">
                            <label class="label">Username:</label>
                            <div class="control">
                                <input class="input" type="text" placeholder="Enter your full name">
                            </div>
                        </div>
                        <!-- <div class="field">
                            <label class="label">Password:</label>
                            <div class="control">
                                <input class="input" type="password" v-model="password" placeholder="Enter your password">
                            </div>
                        </div> -->
                        <!-- <div class="field">
                            <label class="label">Confirm password:</label>
                            <div class="control">
                                <input class="input" type="password" v-model="password" placeholder="Confirm your password">
                            </div>
                        </div> -->
                        <div class="field">
                            <div class="control pt30">
                                <a class="button is-link" value="Register" @click.stop.prevent="register()">
                                    <span>Sign up</span>
                                </a>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import PageTitle from '~/components/PageTitle'
import axios from 'axios'

export default {
    components: {
        PageTitle
    },
    data: function () {
        return {
            email: null,
            password: null,
            type: 'merchant',
        }
    },
    methods: {
        register () {
            axios.
                post('http://localhost:9000/register/', {
                    username: this.name,
                    // password: this.password,
                    type: this.type,
                }, {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(function(res) {
                    console.log("Server response: ", res);
                })
                .catch(function(error) {
                    console.error("Error adding document: ", error);
                });
            // firebase.auth().createUserWithEmailAndPassword(this.email, this.password).catch(function(error) {
            //     var errorCode = error.code;
            //     var errorMessage = error.message;
            //     console.log(error.code)
            //     console.log(error.message)
            // });

            console.log(this.$store.state.user)
        }
    }
};
</script>

<style lang="sass" scoped>


</style>
