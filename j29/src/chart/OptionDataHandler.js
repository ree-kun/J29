import SingleDataPlot from './SingleDataPlot'
import DefaultDataChart from './DefaultDataChart'
import Macd from './Macd'

export default class OptionDataHandler {
    static createOptionChart(optionNumber, chartData, header) {
        switch (optionNumber) {
            case 1:
            case 2:
            case 3:
                return new SingleDataPlot(chartData, header, data => data.get('option' + optionNumber))

            case 5:
                return new Macd(chartData, header, optionNumber)
            default:
                return new DefaultDataChart(chartData, header, optionNumber)
        }
    }
}
