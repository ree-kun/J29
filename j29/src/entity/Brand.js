import Detail from './Detail'
export default class Brand {
    constructor(brand) {
        this.brandCode = brand.brandCode
        this.name = brand.name
        this.stockExchange = brand.stockExchange
        this.detail = new Detail(brand.detail.referenceIndex)
    }

    getName() {
        return this.name
    }

    getBrandCode() {
        return this.brandCode
    }

    getStockExchange() {
        return this.stockExchange
    }
}
