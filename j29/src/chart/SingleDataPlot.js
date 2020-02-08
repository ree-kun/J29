import AbstractChart from './AbstractChart';

export default class SinglePlot extends AbstractChart {
    constructor(chartData, header, createData) {
        super([])
        this.header = header instanceof Array ? header : [header]
        this.createData = createData
        this.data = chartData.map(data => {
            var createdData = this.createData(data)
            return createdData instanceof Array ? createdData : [createdData]
        })
    }
}
