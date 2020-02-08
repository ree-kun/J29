export default class Options {
    constructor(dailyPrices) {
        this.prices = dailyPrices.map(dP => {
            var map = new Map()
            for (var i = 0; i < 32; i++) {
                if (dP['option' + i])
                    map.set('option' + i, dP['option' + i])
            }
            return map
        })
    }
}
