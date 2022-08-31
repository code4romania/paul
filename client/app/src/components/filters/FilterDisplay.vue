<template>
  <div class="filter-display">
    <template v-for="(filter, name) in filterData">
      <b-field
        v-if="filter != null"
        :label="getFieldDef(name).display_name"
        :key="`filterkey-${name}`"
      >
        <div class="tags">
          <b-tag
            v-for="(tag, index) in getValues(filter, name)"
            :key="`tag-${index}`"
            @close="$emit('remove', name, index)"
            close-icon="close"
            :closable="
              isEditable &&
                ((filter.values.length > maxtags && index < maxtags) ||
                  filter.values.length <= maxtags)
            "
            >{{ tag }}</b-tag
          >
        </div>
      </b-field>
    </template>
  </div>
</template>

<script>
import FieldService from '@/services/field'
import { FilterOptions, FilterRelativeDate } from '@/services/field'

export default {
  props: {
    fields: Array,
    filterData: Object,
    isEditable: Boolean
  },
  data() {
    return {
      maxtags: 5
    }
  },
  methods: {
    getFieldDef(name) {
      return (
        this.fields.find(e => e.name == name) || {
          display_name: 'Filter undefined'
        }
      )
    },
    getValues(filter, name) {
      const field_type = this.getFieldDef(name).field_type

      if (typeof filter == 'object') {
        if (filter.blank) return ['Empty values']

        if (filter.values[0] == null) return null

        if (filter.type == 'interval') {
          const values = [
            FieldService.getParsedValue(filter.values[0], field_type),
            FieldService.getParsedValue(filter.values[1], field_type)
          ]

          return [values[0] + ' – ' + values[1]]
        } else if (filter.type == 'relative') {
          return [FilterRelativeDate[filter.values[0]]]
        } else if (filter.type == 'enum') {
          let filterLtd = filter.values.slice(0, this.maxtags)
          if (filter.values.length > this.maxtags)
            filterLtd.push(`+ ${filter.values.length - this.maxtags} more`)

          return filterLtd
        } else
          return [
            (filter.type != 'exact'
              ? FilterOptions[field_type][filter.type] + ' '
              : '') + FieldService.getParsedValue(filter.values[0], field_type)
          ]
      }

      return [filter.toString()]
    }
  }
}
</script>
