<template>
  <div>
    <VField class="field-group">
      <template v-for="(prop, index) in model">
        <b-tooltip type="is-dark" :label="tooltips[index]" :key="index">
          <b-select v-if="options[index]" v-model="model[index]">
            <option
              v-for="(item, key) in options[index]"
              :key="key"
              :value="key"
              v-text="item"
            />
          </b-select>

          <b-input
            v-else
            class="control-input"
            v-model="model[index]"
            maxlength="1"
          />
        </b-tooltip>
      </template>
    </VField>

    <VField label="Drag the elements to match the order of the data you're importing">
      <draggable
        v-model="dateList"
        @change="update"
        draggable=".item"
        class="draggable"
      >
        <template v-for="key in dateList">
          <div
            :key="key"
            class="item"
            v-if="model[key].length"
            v-text="getDisplayValue(key)"
          />
        </template>
      </draggable>
    </VField>
  </div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  props: {
    value: String
  },
  components: {
    draggable
  },
  data() {
    return {
      // 0 - day, 2 - month, 4 - year
      options: {
        0: {
          '': 'None',
          '%d': '01',
          '%w': '1'
        },
        2: {
          '': 'None',
          '%b': 'Jan',
          '%B': 'January',
          '%m': '01'
        },
        4: {
          '': 'None',
          '%y': '70',
          '%Y': '1970'
        }
      },
      tooltips: [
        'Day format',
        'The separator can be a symbol, such as / or .',
        'Month format',
        'The separator can be a symbol, such as / or .',
        'Year format'
      ],
      innerValue: this.value,
      dateList: [0, 1, 2, 3, 4],
      model: ['%d', '/', '%b', '/', '%Y']
    }
  },
  methods: {
    update() {
      const value = this.dateList.map(e => this.model[e])

      this.$emit('input', value.join(''))
    },
    getDisplayValue(key) {
      const value = this.model[key]

      if (this.options[key] != null) return this.options[key][value]
      else return value
    }
  },
  mounted() {
    if (this.value) {
      this.model = ['', '', '', '', '']
      this.dateList = []

      const regex = /(%\w)?(.)?(%\w)?(.)?(%\w)/
      const parsed = this.value.match(regex)
      // console.log(parsed)

      parsed.forEach((e, i) => {
        if (i && e) {
          let found = false

          for (let j = 0; j <= 4; j += 2) {
            if (this.options[j][e]) {
              this.dateList.push(j)
              this.model[j] = e
              found = true
              break
            }
          }

          if (!found) {
            if (!this.model[1].length) {
              this.model[1] = e
              this.dateList.push(1)
            } else if (!this.model[3].length) {
              this.model[3] = e
              this.dateList.push(3)
            }
          }
        }
      })

      if (this.dateList.length < 5) {
        for (let i = 0; i < 5; i++) {
          if (this.dateList.indexOf(i) == -1) this.dateList.push(i)
        }
      }
    }

    this.update()
  },
  watch: {
    model() {
      this.update()
    },
    value(input) {
      this.innerValue = input
    }
  }
}
</script>

<style lang="scss" scoped>
.field-group {
  .control-input {
    margin-right: 0 !important;
    width: 24px;

    /deep/ .input {
      border-color: $grey-select;
    }
  }
}

.draggable {
  border: 1px solid $grey;
  padding: 6px;
  display: inline-block;
  border-radius: $radius-small;

  .item {
    background-color: $grey-select;
    padding: 8px;
    display: inline-block;

    border-radius: $radius-small;
    user-select: none;
    cursor: grab;

    &:hover {
      background-color: $grey-dark;
    }

    &:not(:last-child) {
      margin-right: 8px;
    }
  }
}
</style>
