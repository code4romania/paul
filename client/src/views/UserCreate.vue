<template>
    <div>
        <BaseTitle title="Adaugare utilizator" />
        <BaseCard title="Date utilizator">
            <div class="card-container">
                <ValidationObserver v-slot="{ passes }" tag="form" @submit.prevent>
                    <VField label="Email" rules="required">
                        <b-input v-model="email" />
                    </VField>

                    <b-button
                        native-type="submit"
                        class="button-submit is-primary"
                        @click="passes(submit)"
                    >
                        Creează cont
                    </b-button>
                </ValidationObserver>
            </div>
        </BaseCard>
    </div>
</template>

<script>
import UserService from "@/services/user";
import { ToastService } from "@/services/buefy";


export default {
    data() {
        return {
            email: ''
        }
    },
    methods: {
        submit() {
            this.$store
                .dispatch('registerUser', {
                    email: this.email
                })
                .then(() => {
                    this.$router.replace('users')
                })
        },
        resend() {
            UserService.resend(this.$route.query.confirmation).then(() => {
                ToastService.open('E-mail has been sent')
            })
        }
    }
}
</script>

<style lang="scss" scoped>
.avatar-image {
    width: 140px;
    height: 140px;
}
</style>
