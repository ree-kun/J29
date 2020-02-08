export default class MainChartData {
    constructor(dailyPrice, options) {
        this.data = dailyPrice.prices.map((priceMap, index) => {
            var map = new Map()
            map.set('date', priceMap.get('date'))
            map.set('low', priceMap.get('low'))
            map.set('opening', priceMap.get('opening'))
            map.set('closing', priceMap.get('closing'))
            map.set('high', priceMap.get('high'))
            Array.from(options.prices[index].entries()).forEach(optionValue => {
                return map.set(optionValue[0], optionValue[1])
            })
            return map
        })
    }

    map(mapping) {
        return this.data.map(mapping)
    }
}
