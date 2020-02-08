import React from 'react'
import Chart from 'react-google-charts'

export default class DefaultDataChart {
    constructor(chartData, header, optionNumber) {
        this.optionNumber = optionNumber
        this.header = ['日付', header]
        this.createData = data => [data.get('date'), data.get('option' + optionNumber)]
        this.data = chartData.map(data => this.createData(data))
        console.log(this.data)
    }

    createAxis() {
        return <Chart
            key={"chartAxis" + this.optionNumber}
            chartType="LineChart"
            width="100%"
            height="170px"
            data={[this.header].concat(this.data)}
            options={{
                legend: 'none',
                backgroundColor: 'none',
                chartArea: {left: 100, top: 15, width: '1', height: '100%'}
            }}
        />
    }

    createChart() {
        return <Chart
            key={"chart" + this.optionNumber}
            chartType="LineChart"
            width="100%"
            height="170px"
            data={[this.header].concat(this.data)}
            options={{
                legend: 'none',
                backgroundColor: 'none',
                vAxis: {
                    textPosition: 'none',
                },
                chartArea: {left: 0, top: 15, width: '100%', height: '100%'}
            }}
        />
    }
}
