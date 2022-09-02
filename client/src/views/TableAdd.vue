<template>
  <div>
    <BaseTitle title="Add table" />

    <ValidationObserver v-slot="{ passes }" @submit.prevent slim>
      <BaseCard title="Crează un nou tabel">
        <div class="card-container">
          <div class="columns">
            <div class="column is-6">
              <VField label="Table name" rules="required">
                <b-input v-model="name" />
              </VField>
            </div>
            <div class="column is-6">
              <VField
                label="Cum dorești să creezi noul tabel?"
                name="Table creation type"
                rules="required"
                class="radio-list"
              >
                <b-radio v-model="type" native-value="table-import">
                  Importă fișier CSV
                </b-radio>

                <b-radio v-model="type" native-value="table-edit">
                  Crează în platformă
                </b-radio>
              </VField>
            </div>
          </div>
        </div>

        <template #footer>
          <b-button class="is-primary" @click="passes(submit)"
            >Continuă</b-button
          >
        </template>
      </BaseCard>
    </ValidationObserver>
  </div>
</template>

<script>
export default {
  name: 'TableAdd',
  data() {
    return {
      name: null,
      type: null
    }
  },
  methods: {
    submit() {
      this.$router.push({ name: this.type, query: { name: this.name } })
    }
  }
}
</script>
