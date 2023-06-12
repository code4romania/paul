<template>
  <div>
    <BaseTitle :title="$t('addTable')" />

    <ValidationObserver v-slot="{ passes }" @submit.prevent slim>
      <BaseCard :title="$t('createNewTable')">
        <div class="card-container">
          <div class="columns">
            <div class="column is-6">
              <VField :label="$t('tableNameLabel')" rules="required">
                <b-input v-model="name" />
              </VField>
            </div>
            <div class="column is-6">
              <VField
                :label="$t('howToCreateNewTable')"
                name="Table creation type"
                rules="required"
                class="radio-list"
              >
                <b-radio v-model="type" native-value="table-import">
                  {{ $t('importCSVFile') }}
                </b-radio>

                <b-radio v-model="type" native-value="table-edit">
                  {{ $t('createInPlatform') }}
                </b-radio>

                <b-radio v-model="type" native-value="table-contacts">
                  {{ $t('createEmptyContactsTable') }}
                </b-radio>
              </VField>
            </div>
          </div>
        </div>

        <template #footer>
          <b-button class="is-primary" @click="passes(submit)"
            >{{ $t('continue') }}</b-button
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
      
      if(this.type==='table-contacts')
      {
        this.$store
        .dispatch('data/prepareImportEmptyTable', {'name': this.name}).then(response=>{
          console.log(response);
          // let tmp = JSON.parse(response);
          this.$router.push({ name: 'table-view', params: { idTable: response.id } })
        })
        return;

      }
      this.$router.push({ name: this.type, query: { name: this.name } })
    }
  }
}
</script>
