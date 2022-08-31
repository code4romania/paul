<template>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">
        Filter options

        <span class="info">
          Always click on <b>Set filters</b> after you made your selection.
        </span>
      </p>
      <button type="button" class="delete" @click="$emit('close')" />
    </header>

    <section class="modal-card-body" v-if="table">
      <div class="columns is-gapless">
        <div class="column">
          <b-tabs
            v-model="activeTab"
            class="filter-tabs"
            :animated="false"
            vertical
          >
            <b-tab-item
              v-for="field in table.sorted_fields"
              :key="field.id"
              :label="getFilterLabel(field)"
              :header-class="{
                'is-highlight': filterData[field.name] != null
              }"
            >
              <FilterTypeBase
                v-model="filterData[field.name]"
                v-bind="{ field, filterData }"
                @remove="removeFilter"
              />
            </b-tab-item>
          </b-tabs>
        </div>

        <div class="column is-3 is-scrollable">
          <p class="has-text-weight-semibold is-size-6 cell cell-title">
            Selected filters
          </p>

          <FilterDisplay
            class="cell cell-body"
            :fields="table.fields"
            :filterData="filterData"
            isEditable
            @remove="removeFilter"
          />
        </div>
      </div>
    </section>
    
    <footer class="modal-card-foot">
      <b-button class="is-dark is-outlined" @click="$emit('close')">
        Cancel
      </b-button>
      <b-button class="is-dark" @click="submit">Apply</b-button>
    </footer>
  </div>
</template>

<script>
import FilterDisplay from '@/components/filters/FilterDisplay'
import FilterTypeBase from '@/components/filters/FilterTypeBase'

import { mapState } from 'vuex'

export default {
  name: 'ModalFilters',
  components: {
    FilterDisplay,
    FilterTypeBase
  },
  props: {
    table: Object
  },
  data() {
    return {
      activeTab: 0,
      filterData: {}
    }
  },
  computed: mapState({
    filters: function(state) {
      return state.data.filters[this.table.id]
    }
  }),
  mounted() {
    if (this.filters != null)
      this.filterData = JSON.parse(JSON.stringify(this.filters))
  },
  methods: {
    getFilterLabel(field) {
      let label = field.display_name
      const filter = this.filterData[field.name]

      if (filter != null) {
        if (filter.values.length)
          label += ` (${this.filterData[field.name].values.length})`
        else label += ' (1)'
      }

      return label
    },
    removeFilter(name, index, reset) {
      console.log('removeFilter', name, index, this.filterData[name])

      if (index != null) {
        if (this.filterData[name].values.length > 1) {
          this.$delete(this.filterData[name].values, index)

          this.filterData[name] = {
            ...this.filterData[name]
          }
        } else this.$delete(this.filterData, name)
      } else {
        this.$delete(this.filterData, name)
      }

      if (reset != null) reset()
    },
    submit() {
      this.$store.commit('data/setFilters', {
        idTable: this.table.id,
        filter: this.filterData
      })
      this.$emit('submit')
      this.$emit('close')
    }
  }
}
</script>

<style lang="scss" scoped>
$cell-padding: 18px 24px;

.modal-card {
  @include desktop {
    max-width: 1200px;
    width: 90vw;
    height: 60vh;
  }

  .modal-card-head {
    border-bottom: 1px solid $grey-lighter;
  }

  .modal-card-foot {
    border-top: 1px solid $grey-lighter;
  }

  .modal-card-body {
    padding: 0;
    display: flex;
    overflow: hidden;

    .cell {
      padding: $cell-padding;

      &.cell-title {
        background-color: $white;
        position: sticky;
        top: 0;
        z-index: 1;
      }

      &.cell-body {
        padding-top: 0;
      }
    }

    .is-scrollable {
      overflow-y: auto;
    }

    .columns {
      flex: 1;
      align-items: stretch;
      margin-bottom: 0 !important;

      .column {
        position: relative;

        &:last-child {
          border-left: 1px solid $grey-lighter;
        }
      }
    }
  }
}
</style>
