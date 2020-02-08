export default class Detail {
    constructor(detail) {
        if (detail.marketCapitalization) {
            this.kind = 'listedCompany'
            this.marketCapitalization = detail.marketCapitalization
            this.commonSharesOutstanding = detail.commonSharesOutstanding
            this.dividendYield = detail.dividendYield
            this.dividendPerShare = detail.dividendPerShare
            this.priceEarningsRatio = detail.priceEarningsRatio
            this.priceBookvalueRatio = detail.priceBookvalueRatio
            this.earningsPerShare = detail.earningsPerShare
            this.bookvaluePerShare = detail.bookvaluePerShare
            this.minPurchaseValue = detail.minPurchaseValue
            this.shareUnitNumber = detail.shareUnitNumber
            this.yearToDateHigh = detail.yearToDateHigh
            this.yearToDateLow = detail.yearToDateLow
        } else if (detail.netAsset) {
            this.kind = 'investmentTrust'
            this.netAsset = detail.netAsset
            this.minPurchaseValue = detail.minPurchaseValue
            this.tradingUnit = detail.tradingUnit
            this.yearToDateHigh = detail.yearToDateHigh
            this.yearToDateLow = detail.yearToDateLow
            this.managementCompany = detail.managementCompany
            this.investmentAsset = detail.investmentAsset
            this.investmentArea = detail.investmentArea
            this.interlockTarget = detail.interlockTarget
            this.accountingCount = detail.accountingCount
            this.accountingMonth = detail.accountingMonth
            this.listedDate = detail.listedDate
            this.custodianFee = detail.custodianFee
        }
    }

    getDetailList() {
        switch (this.kind) {
            case 'listedCompany':
                return [
                    ['参考指標', ''],
                    ['時価総額', this.getMarketCapitalization()],
                    ['発行済株式数', this.getCommonSharesOutstanding()],
                    ['配当利回り', this.getDividendYield()],
                    ['1株配当', this.getDividendPerShare()],
                    ['PER', this.getPriceEarningsRatio()],
                    ['PBR', this.getPriceBookvalueRatio()],
                    ['EPS', this.getEarningsPerShare()],
                    ['BPS', this.getBookvaluePerShare()],
                    ['最低購入代金', this.getMinPurchaseValue()],
                    ['単元株数', this.getShareUnitNumber()],
                    ['年初来高値', this.getYearToDateHigh()],
                    ['年初来安値', this.getYearToDateLow()]
                ]
            case 'investmentTrust':
                return [
                    ['参考指標', ''],
                    ['純資産', this.getNetAsset()],
                    ['最低購入代金', this.getMinPurchaseValue()],
                    ['売買単位', this.getTradingUnit()],
                    ['年初来高値', this.getYearToDateHigh()],
                    ['年初来安値', this.getYearToDateLow()],
                    ['運用会社', this.getManagementCompany()],
                    ['投資対象資産', this.getInvestmentAsset()],
                    ['投資対象地域', this.getInvestmentArea()],
                    ['連動対象', this.getInterlockTarget()],
                    ['決算頻度', this.getAccountingCount()],
                    ['決算月', this.getAccountingMonth()],
                    ['上場年月日', this.getListedDate()],
                    ['信託報酬', this.getCustodianFee()]
                ]
            default:
                return null
        }
    }


    static formatValue(index, value) {
        var formattes = [
            ["", "百万円"],
            ["", "株"],
            ["", "%"],
            ["", ""],
            ["", "倍"],
            ["", "倍"],
            ["", ""],
            ["", ""],
            ["", "円"],
            ["", "株"],
            ["", "円"],
            ["", "円"],

            ["", "百万円"],
            ["", "株"],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", "回"],
            ["", "月"],
            ["", ""],
            ["", "%"],
        ]
        var format = formattes[index]
        return format[0] + value + format[1]
    }

    getMarketCapitalization() {
        return Detail.formatValue(0, this.marketCapitalization)
    }

    getCommonSharesOutstanding() {
        return Detail.formatValue(1, this.commonSharesOutstanding)
    }

    getDividendYield() {
        return Detail.formatValue(2, this.dividendYield)
    }

    getDividendPerShare() {
        return Detail.formatValue(3, this.dividendPerShare)
    }

    getPriceEarningsRatio() {
        return Detail.formatValue(4, this.priceEarningsRatio)
    }

    getPriceBookvalueRatio() {
        return Detail.formatValue(5, this.priceBookvalueRatio)
    }

    getEarningsPerShare() {
        return Detail.formatValue(6, this.earningsPerShare)
    }

    getBookvaluePerShare() {
        return Detail.formatValue(7, this.bookvaluePerShare)
    }

    getMinPurchaseValue() {
        return Detail.formatValue(8, this.minPurchaseValue)
    }

    getShareUnitNumber() {
        return Detail.formatValue(9, this.shareUnitNumber)
    }

    getYearToDateHigh() {
        return Detail.formatValue(10, this.yearToDateHigh)
    }

    getYearToDateLow() {
        return Detail.formatValue(11, this.yearToDateLow)
    }

    getNetAsset() {
        return Detail.formatValue(12, this.netAsset)
    }

    getTradingUnit() {
        return Detail.formatValue(13, this.tradingUnit)
    }

    getManagementCompany() {
        return Detail.formatValue(14, this.managementCompany)
    }

    getInvestmentAsset() {
        return Detail.formatValue(15, this.investmentAsset)
    }

    getInvestmentArea() {
        return Detail.formatValue(16, this.investmentArea)
    }

    getInterlockTarget() {
        return Detail.formatValue(17, this.interlockTarget)
    }

    getAccountingCount() {
        return Detail.formatValue(18, this.accountingCount)
    }

    getAccountingMonth() {
        return Detail.formatValue(19, this.accountingMonth)
    }

    getListedDate() {
        return Detail.formatValue(20, this.listedDate)
    }

    getCustodianFee() {
        return Detail.formatValue(21, this.custodianFee)
    }
}
