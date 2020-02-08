import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Chart from 'react-google-charts'
import AbstractChart from '../chart/AbstractChart'
import Candlestick from '../chart/Candlestick'
import OptionDataHandler from '../chart/OptionDataHandler'

export default class MainChartArea extends Component {
  constructor(props) {
    super(props)
    this.state = {}
  }

  static getDerivedStateFromProps(nextProps, prevState) {
    var loadOptions = nextProps.loadOptions
    var nextState = prevState
    var chartData = nextProps.chartData
    if (nextProps.shouldChange) {
      nextState.candlestick = new Candlestick(chartData)
    }

    for (var i = 1; i < 32; i++) {
      if (loadOptions.code >> i & true)
        nextState['option' + i] = OptionDataHandler.createOptionChart(i, chartData, loadOptions.name[i])
    }

    return nextState
  }

  mousemove(event) {
    // 要素の位置を取得
    // var target = document.getElementById('supportLinesMouseMove')
    var target = document.getElementById('supportLinesWrapper')
    var clientRect = target.getBoundingClientRect()
    var positionX = event.clientX - clientRect.left
    var positionY = event.clientY - clientRect.top

    var horizontal = document.getElementById('horizontalLine')
    var vertical = document.getElementById('verticalLine')
    var areaTopLeft = document.getElementById('areaTopLeft')
    var areaTopRight = document.getElementById('areaTopRight')
    var areaBottomLeft = document.getElementById('areaBottomLeft')
    var areaBottomRight = document.getElementById('areaBottomRight')
    horizontal.style.height = positionY + 'px'
    horizontal.style.width = '100%'
    vertical.style.height = '100%'
    vertical.style.width = positionX + 'px'

    areaTopLeft.style.height = positionY + 1 + 'px'
    areaTopLeft.style.width = positionX - 1 + 'px'
    areaTopRight.style.height = positionY - 2 + 'px'
    areaTopRight.style.left = positionX - 1 + 'px'
    areaTopRight.style.right = 0 + 'px'
    areaBottomLeft.style.top = positionY + 1 + 'px'
    areaBottomLeft.style.bottom = 0 + 'px'
    areaBottomLeft.style.width = positionX + 1 + 'px'
    areaBottomRight.style.top = positionY - 2 + 'px'
    areaBottomRight.style.bottom = 0 + 'px'
    areaBottomRight.style.left = positionX + 1 + 'px'
    areaBottomRight.style.right = 0 + 'px'
  }

  render() {
    var brand = this.props.brand

    var subData = []
    var displayOptions = this.props.displayOptions
    for (var i = 1; i <= 3 ; i++) {
      if (displayOptions >> i & true)
        subData.push(this.state['option' + i])
    }
    var displayData = AbstractChart.merge(this.state.candlestick, subData)
    var width = displayData.data.length / 60 * 100
    return (
      <div className="wrapper">
        <div id="brand">
          <h1>{brand.getName()}</h1>
        </div>
        <div className="chart">
          {/* https://react-google-charts.com/ */}
          {/* 軸を表示するだけのコンポーネント */}
          <div className="axis">
            <Chart
              chartType="ComboChart"
              height="350px"
              data={this.state.candlestick.getData()}
              options={{
                seriesType: 'candlesticks',
                legend: 'none',
                series: {
                  1: {type: 'line', curveType: 'function'},
                  2: {type: 'line', curveType: 'function'},
                  3: {type: 'line', curveType: 'function'},
                  4: {type: 'line', curveType: 'function'}
                },
                backgroundColor: 'none',
                hAxis: {
                  textPosition: 'none'
                },
                chartArea: {left: 100, top: 15, width: '1', height: '100%'}
              }}
            />
            {(() => {
              var chartAxes = []
              for (var i = 4; i < 32; i++) {
                chartAxes.push(
                  displayOptions >> i & true ?
                    this.state["option" + i].createAxis() : ""
                )
              }
              return chartAxes
            })()}
          </div>
          {/* チャートを表示するコンポーネント */}
          <div className="figure scrollable">
            {(() => {
              var count = displayData.data.length / 20
              var minorGridlines = []
              for (let i = 1; i <= count; i++) {
                minorGridlines.push(<div key={i} className="minorGrildline"  style={{width: (i * 20 + 0.5) / 60 * 100 + '%'}}></div>)
              }
              return minorGridlines
            })()}
            <div id="supportLinesWrapper" style={{width: width + '%'}}>
              <div id="supportLines" onMouseMove={(event) => this.mousemove(event)}>
                <div id="horizontalLine"></div>
                <div id="verticalLine"></div>
              </div>
            </div>
            <div style={{width: width + '%', height: '100%'}}>
              <Chart
                chartType="ComboChart"
                width="100%"  // チャート全体の大きさ（A)
                height="350px"
                data={displayData.getData()}
                options={{
                  seriesType: 'candlesticks',
                  legend: 'none',
                  series: {
                    1: {type: 'line', curveType: 'function'},
                    2: {type: 'line', curveType: 'function'},
                    3: {type: 'line', curveType: 'function'},
                    4: {type: 'line', curveType: 'function'},
                    5: {type: 'line', curveType: 'function'}
                  },
                  backgroundColor: 'none',
                  vAxis: {
                    textPosition: 'none',
                  },
                  hAxis: {
                    textPosition: 'in',
                    showTextEvery: 20
                  },
                  chartArea: {left: 0, top: 15, width: '100%', height: '100%'} // データをプロットしている部分だけの大きさ。（Aとの比）
                }}
              />
              {(() => {
                var charts = []
                for (var i = 4; i < 32; i++) {
                  charts.push(
                    displayOptions >> i & true ?
                      this.state["option" + i].createChart() : ""
                  )
                }
                return charts
              })()}
            </div>
            <div id="supportLinesMouseMove" style={{width: width + '%'}}>
              <div id="areaTopLeft" onMouseMove={(event) => this.mousemove(event)}></div>
              <div id="areaTopRight" onMouseMove={(event) => this.mousemove(event)}></div>
              <div id="areaBottomLeft" onMouseMove={(event) => this.mousemove(event)}></div>
              <div id="areaBottomRight" onMouseMove={(event) => this.mousemove(event)}></div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

MainChartArea.propTypes = {
  brand: PropTypes.object.isRequired,
  chartData: PropTypes.object.isRequired,
  shouldChange: PropTypes.bool.isRequired,
  loadOptions: PropTypes.object.isRequired,
  displayOptions: PropTypes.number.isRequired
}
