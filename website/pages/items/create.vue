<template>
    <section class="is-medium is-full-height">
        <div class="container is-flex justify-center align-center is-full-height">
            <div class="box">
                <h2>Add an item {{ ip }}</h2>
                <form action="">
                    <div class="field">
                        <label class="label">Name:</label>
                        <div class="control">
                            <input class="input" type="text" v-model="name" placeholder="Enter item name">
                        </div>
                        <!-- <p class="help">This is a help text</p> -->
                    </div>
                    <div class="field">
                        <label class="label">Quantity:</label>
                        <div class="control">
                            <input class="input" type="text" v-model="qty" placeholder="Enter item quantity">
                        </div>
                        <!-- <p class="help">This is a help text</p> -->
                    </div>
                    <div class="field">
                        <label class="label">Shelf:</label>
                        <div class="control">
                            <input class="input" type="text" v-model="shelf" placeholder="Enter which shelf">
                        </div>
                        <!-- <p class="help">This is a help text</p> -->
                    </div>
                    <div class="field">
                        <div class="control">
                            <input type="submit" class="button is-link" value="Add item"  @click.stop.prevent="addItem()">
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </section>
</template>

<script>
// import firebase, {auth} from '~/services/fireinit'
import axios from 'axios'

export default {
    data: function () {
        return {
            name: null,
            qty: null,
            shelf: null,
            ip: null
        }
    },
    methods: {
        addItem: function () {
            axios.
                post('http://localhost:9000/items/', {
                    name: this.name,
                    qty: this.qty,
                    shelf: this.shelf,
                }, {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(function(docRef) {
                    console.log("Document written with ID: ", docRef);
                })
                .catch(function(error) {
                    console.error("Error adding document: ", error);
                });
            
            // firebase.firestore().collection("items").add({
            //     name: this.name,
            //     qty: this.qty,
            //     shelf: this.shelf,
            // })
            // .then(function(docRef) {
            //     console.log("Document written with ID: ", docRef.id);
            // })
            // .catch(function(error) {
            //     console.error("Error adding document: ", error);
            // });
        },
        // async fetchSomething() {
        //     const ip = await this.$axios.$get('http://icanhazip.com')
        //     this.ip = ip
        // }
    },
    mounted: function () {
        // this.fetchSomething()
        console.log('opa')
    }
};
</script>

<style lang="sass" scoped>

    .box
        width: 32rem    

</style>
