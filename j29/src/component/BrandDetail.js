import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Chart from 'react-google-charts'

export default class BrandDetail extends Component {
    constructor(props) {
      super(props)
    }
  
    render() {
      var detail = this.props.brand.detail
      return (
        <div className="chart">
          {/* https://react-google-charts.com/ */}
          <Chart
            chartType="Table"
            width="100%"
            height="100%"
            data={detail.getDetailList()}
            options={{
              showRowNumber: true,
            }}
          />
        </div>
      )
    }
  }
  
  BrandDetail.propTypes = {
    brand: PropTypes.object.isRequired
  }
  
  