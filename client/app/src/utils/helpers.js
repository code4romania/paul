// import router from '@/router/'

const NumberFormat = x => {
  return x.toLocaleString('ro-RO', {
    maximumFractionDigits: 2
  })
}

const Parser = {
  date: date =>
    date ? new Date(date).toLocaleDateString('ro-RO').replace(/\./g, '/') : '',
  datetime: date =>
    date ? new Date(date).toLocaleString('ro-RO').replace(/\./g, '/') : '',
  int: NumberFormat,
  float: NumberFormat
}

const QueryString = function(params) {
  return Object.keys(params)
    .map(key => key + '=' + encodeURIComponent(params[key]))
    .join('&')
}

const FilterQuery = function(filterData) {
  const query = {}

  Object.keys(filterData).forEach(key => {
    let e = filterData[key]

    console.log('filterData', key, e)
    if (e != null) {
      if (e.blank) {
        query[key] = '__BLANK'
      } else if (e.type == 'enum' && e.values.length) {
        query[key] = e.values.join(',')
      } else if (e.type == 'interval') {
        query[`${key}__gte`] = e.values[0]
        query[`${key}__lte`] = e.values[1]
      } else {
        query[`${key}__${e.type}`] = e.values[0]
      }
    }
  })

  return query
}

export { Parser, QueryString, FilterQuery }
