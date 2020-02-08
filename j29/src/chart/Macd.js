import React from 'react'
import Chart from 'react-google-charts'

export default class Macd {
    constructor(chartData, header, optionNumber) {
        this.header = ['日付', header, 'シグナル', '', '']
        this.createData = data => {
            var optionData = data.get('option' + optionNumber)
            var macd = optionData ? optionData['macd'] : optionData
            var signal = optionData ? optionData['signal'] : optionData
            var diff = (macd && signal) ? macd - signal : 0
            return [data.get('date'), macd, signal, diff > 0 ? diff : undefined, diff < 0 ? diff : undefined]
        }
        this.data = chartData.map(data => this.createData(data))
    }

    createAxis() {
        return <Chart
            key={"chartAxis" + this.optionNumber}
            chartType="ComboChart"
            width="100%"
            height="170px"
            data={[this.header].concat(this.data)}
            options={{
                seriesType: 'line',
                legend: 'none',
                isStacked: true,
                series: {
                  2: {type: 'bars'},
                  3: {type: 'bars'}
                },
                backgroundColor: 'none',
                chartArea: {left: 100, top: 15, width: '1', height: '100%'}
            }}
        />
    }

    createChart() {
        return <Chart
            key={"chart" + this.optionNumber}
            chartType="ComboChart"
            width="100%"
            height="170px"
            data={[this.header].concat(this.data)}
            options={{
                seriesType: 'line',
                legend: 'none',
                isStacked: true,
                series: {
                  2: {type: 'bars'},
                  3: {type: 'bars'}
                },
                backgroundColor: 'none',
                vAxis: {
                    textPosition: 'none',
                },
                chartArea: {left: 0, top: 15, width: '100%', height: '100%'}
            }}
        />
    }
}
