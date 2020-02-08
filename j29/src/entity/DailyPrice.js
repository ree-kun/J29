export default class DailyPrice {
    constructor(dailyPrices) {
        this.prices = dailyPrices.map(dP => {
            var map = new Map()
            map.set('date', dP.date)
            map.set('low', dP.lowPrice)
            map.set('opening', dP.openingPrice)
            map.set('closing', dP.closingPrice)
            map.set('high', dP.highPrice)
            return map
        })
    }

    getPrices() {
        return this.prices
    }
}
