Apex.dataLabels = {
  enabled: false
}

var colorPalette = ['#08a6a1']

var optionsBar = {
  chart: {
    type: 'bar',
    height: 380,
    width: '100%',
    stacked: true,
  },
  plotOptions: {
    bar: {
      columnWidth: '45%',
    }
  },
  colors: colorPalette,
  series: [{
    name: "Order",
    data: [42, 52, 16, 55, 59, 51, 45, 32, 26, 33, 42, 52, 16, 55, 59, 51, 45, 32, 26, 33, 42, 52, 16, 55, 59, 51, 45, 32, 26, 10],
  }],
  labels: ['1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021', '1 Jan 2021'],
  xaxis: {
    labels: {
      show: false
    },
    axisBorder: {
      show: true
    },
    axisTicks: {
      show: false
    },
    axisLine: {
      show: false
    }
  },
  yaxis: {
    axisBorder: {
      show: true
    },
    axisTicks: {
      show: true
    },
    labels: {
      style: {
        color: '#a0a0a0'
      }
    }
  },
  grid: {
    show: true,
    borderColor: '#f0f0f0',
  }
}

var chartBar = new ApexCharts(document.querySelector('#bar'), optionsBar);
chartBar.render();