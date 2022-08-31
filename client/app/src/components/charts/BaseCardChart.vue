<template>
  <div class="card card-chart" v-if="data != null">
    <div class="card-header">
      <p class="is-size-6 has-text-weight-semibold">{{ title }}</p>
    </div>
    <div class="card-body">
      <h2 class="card-number">{{ data | parseNumber }}</h2>
      <b-icon icon="flag-outline" class="card-icon" />
    </div>
  </div>
</template>

<script>
// import { mapState } from 'vuex'

export default {
  components: {},
  props: {
    data: Number,
    title: String
  },
  data() {
    return {}
  },
  computed: {},
  mounted() {},
  methods: {}
}
</script>
