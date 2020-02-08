import AbstractChart from './AbstractChart'

export default class Candlestick extends AbstractChart {
    constructor(chartData) {
        super(chartData)
        this.header = ['日付','株価','','','']
    }

    createData(data) {
        return [data.get('date'),
                data.get('low'),
                data.get('opening'),
                data.get('closing'),
                data.get('high')]
    }
}
