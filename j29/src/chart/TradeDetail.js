import AbstractChart from './AbstractChart'

export default class TradeDetail extends AbstractChart {
    constructor(chartData) {
        super(chartData)
        this.header = ['取引詳細','出来高']
    }

    createData(data) {
        return [data.get('date'),
                data.get('volume')]
    }
}
