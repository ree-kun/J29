export default class AbstractChart {
    constructor(chartData) {
        this.header = []
        this.data = chartData.map(data => this.createData(data))
    }

    createData() {
        return null
    }

    add(olderChartData) {
        this.data = olderChartData.map(data => this.createData(data))
                    .concat(this.data)
        return this
    }

    getData() {
        return [this.header].concat(this.data)
    }

    static merge(mainChartData, subChartDatas) {
        var mergedChartData = new AbstractChart([])
        mergedChartData.header = mainChartData.header
                                    .concat(subChartDatas.flatMap(chartData => chartData.header))
        mergedChartData.data = mainChartData.data.map(
            (currentValue, index) => {
                var subData = subChartDatas.flatMap(chartData => {
                    return chartData.data[index]
                })

                return currentValue.concat(subData)
            })
        return mergedChartData
    }
}
