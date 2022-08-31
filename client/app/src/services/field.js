import { Parser } from '@/utils/helpers'
import getNestedObj from 'lodash.get'

const FieldComponentMap = {
  enum: 'VSelect',
  // bool: 'b-checkbox',
  date: 'VDate'
}

const FieldFilterComponentMap = {
  enum: 'FilterTypeEnum',
  // bool: 'b-checkbox',
  date: 'FilterTypeDate',
  int: 'FilterTypeNumeric',
  float: 'FilterTypeNumeric'
}

const FieldTypes = {
  enum: 'Enumerare (Set de opțiuni predefinite)',
  date: 'Dată',
  int: 'Număr întreg',
  float: 'Număr cu zecimale',
  // bool: 'Yes/No',
  text: 'Text'
}

const FilterOptionsNumeric = {
  // blank: 'Empty or "blank" fields',
  gt: 'Greater than',
  gte: 'Greater than or equal',
  lt: 'Lower than',
  lte: 'Lower than or equal',
  exact: 'Equal to',
  interval: 'Interval'
}

const FilterOptions = {
  int: FilterOptionsNumeric,
  float: FilterOptionsNumeric,
  date: {
    gt: 'After date',
    gte: 'After date, including',
    lt: 'Before date',
    lte: 'Before date, including',
    exact: 'Exact date',
    interval: 'Date interval',
    relative: 'Relative time'
  },
  text: {
    icontains: ''
  }
}

const FilterRelativeDate = {
  last_day: 'Yesterday',
  next_day: 'Tomorrow',
  current_day: 'Today',
  last_week: 'Last week',
  next_week: 'Next week',
  current_week: 'This week',
  last_month: 'Last month',
  next_month: 'Next month',
  current_month: 'This month',
  last_year: 'Last year',
  next_year: 'Next year',
  current_year: 'This year'
}

const FieldService = {
  getColumns() {},
  getParsedValue(value, type) {
    return Parser[type] ? Parser[type](value) : value
  },
  getFieldTypes() {
    return FieldTypes
  },
  getComponent(type) {
    return FieldComponentMap[type] ? FieldComponentMap[type] : 'VInput'
  },

  getFilterComponent(type) {
    return FieldFilterComponentMap[type]
      ? FieldFilterComponentMap[type]
      : 'FilterTypeText'
  },

  getSortFunction(field) {
    return (a, b, isAsc) => {
      let x = getNestedObj(a.data, field)
      let y = getNestedObj(b.data, field)

      const order = isAsc ? 1 : -1

      if (x === y) return 0
      else return x > y ? order : -order
    }
  },

  isNumeric(field) {
    return ['int', 'float'].indexOf(field.field_type) != -1
  }
}

export default FieldService

export { FilterOptions, FilterRelativeDate }
