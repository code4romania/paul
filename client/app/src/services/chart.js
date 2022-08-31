const ChartTypes = {
  Bar: 'Bar',
  Line: 'Line',
  Pie: 'Pie',
  Doughnut: 'Doughnut'
}

const ChartFunctions = {
  Count: 'Count',
  Sum: 'Sum',
  Avg: 'Average',
  Max: 'Maximum',
  Min: 'Minimum'
}

const ChartTimelineGroup = {
  minute: 'Minute',
  hour: 'Hour',
  day: 'Day',
  week: 'Week',
  month: 'Month',
  year: 'Year'
}

const ChartConfig = {
  getChartTypes() {
    return ChartTypes
  },
  getComponent(type) {
    return ChartTypes[type] ? 'Chart' + ChartTypes[type] : 'ChartBar'
  },
  getFunctions() {
    return ChartFunctions
  },
  getTimelineGroups() {
    return ChartTimelineGroup
  }
}

export default ChartConfig
