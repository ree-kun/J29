import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import PropTypes from 'prop-types'
import Brand from './entity/Brand'
import DailyPrice from './entity/DailyPrice'
import Options from './entity/Options'
import MainChartArea from './component/MainChartArea'
import BrandDetail from './component/BrandDetail'
import MainChartData from './entity/chartData/MainChartData'
import './style.css'
import './css/bootstrap.min.css'
import { DropdownButton, Form } from 'react-bootstrap';

class SearchConditions extends Component {
  constructor(props) {
    super(props)
    this.state = {brandCode: "", options: [], loadedOptions: [], date: ""}
  }

  onChangeCode(event) {
    var options = this.state.options
    options[0] = {checked: true}
    this.setState({brandCode: event.target.value,
                   options: options,
                   loadedOptions: [this.state.brandCode == this.state.loadedBrandCode]})
  }

  onChangeOptions(event) {
    var options = this.state.options
    var optionNumber = event.target.value
    var checked = event.target.checked

    options[optionNumber] = {checked: checked, name: event.target.nextElementSibling.innerHTML}
    this.setState({options: options})
    if (this.state.loaded) {
      // このifは意味不明
      if (checked && !this.state.loadedOptions[optionNumber]) {
        this.requestApi()
        return
      } else {
        this.requestApi()
      }
    }
  }

  onClickSubmit() {
    this.requestApi(() => this.setState({loaded: true}))
  }

  requestApi(success = () => {}, fail = () => {}) {
    var conditions = getConditions(this)
    var brandCode = conditions.brandCode
    var options = conditions.options
    var changedBrandCode = brandCode != this.state.loadedBrandCode
    console.log(`https://www.ryoito.shop/api/brandInfo/?brandCode=${brandCode}&options=${options.code}`)
    fetch(`https://www.ryoito.shop/api/brandInfo/?brandCode=${brandCode}&options=${options.code}&format=json`)
    .then((response) => response.json())
    .then((json) => {
      var result = json[0]
      success()

      this.props.setBrandInfo(result, changedBrandCode, options, this.optionsIntegration(this.state.options.map(option => option.checked)))
    })
    .catch((response) => {
      console.log('** error **', response)
      fail()
    })

    function getConditions(component) {
      var brandCode = changeFullWidthToHalfWidthChar(component.state.brandCode)
      component.setState({loadedBrandCode: brandCode})

      // ここの処理はsuccessメソッドの中に入れたい
      var loadedOptions = Array.from(component.state.loadedOptions)
      component.state.options
          .forEach((option, index) => loadedOptions[index] = option.checked || component.state.loadedOptions[index])
      component.setState({loadedOptions: loadedOptions})

      return {
        brandCode: brandCode,
        options: {code: component.optionsIntegration(
            component.state.options.map(option => option.checked))
            & ~component.optionsIntegration(component.state.loadedOptions),
        name: component.state.options.map(option => option.name)}
      }

      function changeFullWidthToHalfWidthChar(halfWidthChar) {
        return halfWidthChar.replace(/[０-９]/g, (s) => String.fromCharCode(s.charCodeAt(0) - 65248))
      }
    }
  }

  optionsIntegration(options) {
    return options ?
        options.reduce(
          (accumulator, option, index) => (accumulator + (option << index)), 0)
        : 0
  }

  render() {
    return (
      <div className="wrapper">
        <DropdownButton id="dropdown-trend-button" title="トレンド系">
          <Form.Check className="checkBox" inline value="1" name="movingAverageLine5"
              onClick={(event) => this.onChangeOptions(event)} label="5日移動平均線" />
          <Form.Check className="checkBox" inline value="2" name="movingAverageLine10"
              onClick={(event) => this.onChangeOptions(event)} label="10日移動平均線" />
          <Form.Check className="checkBox" inline value="3" name="movingAverageLine15"
              onClick={(event) => this.onChangeOptions(event)} label="15日移動平均線" />
        </DropdownButton>
        <DropdownButton id="dropdown-oscillator-button" title="オシレーター系">
          {/* <Form.Check className="checkBox" inline value="4" name="priceDerivative"
              onClick={(event) => this.onChangeOptions(event)} label="株価変化度" /> */}
          <Form.Check className="checkBox" inline value="5" name="macd"
              onClick={(event) => this.onChangeOptions(event)} label="MACD" />
          <Form.Check className="checkBox" inline value="6" name="rsi"
              onClick={(event) => this.onChangeOptions(event)} label="RSI" />
        </DropdownButton>
        <fieldset style={{padding: "4px 7px"}}>
          <div>
            <input type="text" value={this.state.brandCode}
              onChange={(event) => this.onChangeCode(event)} placeholder="銘柄コード"
              onKeyPress={() => {
                if ( window.event.keyCode == 13 ) {
                  this.onClickSubmit()}}} />
              <input className="btn btn-info" type="submit" value="検索"
                onClick={() => this.onClickSubmit()} />
              <a className="btn btn-primary" href="./architecture.html" title="システム構成図"
                target="_blank" style={{marginLeft: "30px", padding: "4px 7px"}}>システム構成図はこちら</a>
          </div>
        </fieldset>
      </div>
    )
  }
}

SearchConditions.propTypes = {
  setBrandInfo: PropTypes.func.isRequired
}

ReactDOM.render(
  <SearchConditions setBrandInfo={(brandInfo, isChanged, loadOptions, displayOptions) => setBrandInfo(brandInfo, isChanged, loadOptions, displayOptions)} />,
  document.getElementById('menu')
)

function setBrandInfo(brandInfo, isChanged, loadOptions, displayOptions) {
  if (brandInfo) {
    var brand = new Brand(brandInfo.brand)
    var dailyPrices = new DailyPrice(brandInfo.dailyPrices)
    var options = new Options(brandInfo.dailyPrices)
  }

  ReactDOM.render(
    <MainChartArea brand={brand} chartData={new MainChartData(dailyPrices, options)} shouldChange={isChanged} loadOptions={loadOptions} displayOptions={displayOptions} />,
    document.getElementById('displayChart')
  )
  ReactDOM.render(
    <BrandDetail brand={brand} />,
    document.getElementById('brandDetail')
  )
}
