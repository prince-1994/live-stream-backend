<template>
    <div class="page-signup">
        <div class="container">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Log In</h1>
                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label for="">Email</label>
                        <div class="control">
                            <input
                                type="email"
                                name="username"
                                class="input"
                                v-model="username"
                            />
                        </div>
                    </div>

                    <div class="field">
                        <label for="">Password</label>
                        <div class="control">
                            <input
                                type="password"
                                name="password"
                                class="input"
                                v-model="password"
                            />
                        </div>
                    </div>

                    <div class="notiication is-danger" v-if="error.length">
                        <p v-for="error in errors" v-bind:key="error">
                            {{ error }}
                        </p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-success">Log In</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "SignUp",
    data() {
        return {
            username: "",
            password: "",
            error: [],
        };
    },
    methods: {
        submitForm(e) {
            axios.defaults.headers.common["Authorization"] = "";
            const formData = {
                username: this.username,
                password: this.password,
            };
            axios
                .post("auth/token/login/", formData)
                .then((response) => {
                    console.log(response);
                    const token = response.data.auth_token;
                    this.$store.commit("setToken", token);
                    axios.defaults.headers.common["Authorization"] =
                        "Token " + token;
                    localStorage.setItem("token", token);
                    this.$router.push("/dashboard");
                })
                .catch((error) => {
                    console.log(error);
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(
                                `${property}:${error.response.data[property]}`
                            );
                        }
                        console.log(JSON.stringify(error.response.data));
                    } else if (error.message) {
                        console.log(JSON.stringify(error.message));
                    } else {
                        console.log(JSON.stringify(error));
                    }
                });
        },
    },
};
</script>