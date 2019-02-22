<template>
    <div>

        <page-title
            title="List of all items"
        ></page-title>
        <section class="section">
            <div class="container">
                <div class="box is-full-width">
                    <table class="table is-full-width">
                        <thead>
                            <tr>
                                <td class="quarter-width">Item name</td>
                                <td>Quantity</td>
                                <td>Shelf</td>
                                <td>View details</td>
                                <td>Edit item</td>
                                <td>Delete item</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in items" :key="item.id">
                                <td>
                                    <b>{{ item.name }}</b>
                                </td>
                                <td>
                                    {{ item.qty }}
                                </td>
                                <td>
                                    {{ item.shelf }}
                                </td>
                                <td>
                                    <a href="#" class="has-text-info">
                                        <i class="mdi mdi-eye"></i>
                                        View
                                    </a>
                                </td>
                                <td>
                                    <a href="#" class="has-text-success">
                                        <i class="mdi mdi-pencil"></i>
                                        Edit
                                    </a>
                                </td>
                                <td>
                                    <a href="#" class="has-text-danger">
                                        <i class="mdi mdi-delete"></i>
                                        Delete
                                    </a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
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
            items: []
        }
    },
    methods: {
        getItems: function () {
            axios.
                get('/items')
                .then((res) => {
                    this.items = res.items
                    console.log(res)
                })
                .catch(function (res) {
                    console.log(res)
                })
            // firebase.firestore().collection("items").get().then((querySnapshot) => {
            //     this.items = []
            //     querySnapshot.forEach((doc) => {
            //         let item = doc.data()
            //         item._id = doc.id
            //         this.items.push(item)
            //     });
            // });
        }
    },
    mounted: function () {
        this.getItems()
    }
};
</script>

<style lang="sass" scoped>

    // .box
    //     width: 32rem    

</style>
