
const CHART_COLORS = {
  red: 'rgb(255, 99, 132)',
  orange: 'rgb(255, 159, 64)',
  yellow: 'rgb(255, 205, 86)',
  green: 'rgb(75, 192, 192)',
  blue: 'rgb(54, 162, 235)',
  purple: 'rgb(153, 102, 255)',
  grey: 'rgb(201, 203, 207)'
};
const CHART_COLORS_LIST = [
  'rgb(255, 99, 132)',
  'rgb(75, 192, 192)',
  'rgb(54, 162, 235)',
  'rgb(255, 159, 64)',
  'rgb(255, 205, 86)',
  'rgb(153, 102, 255)',
  'rgb(0, 154, 255)',
  'rgb(31, 223, 134)'
];

const createPieChart =  (chartId, chartTitle, chartData)  => {
  const _items = chartData.items
  const _countries = _items.map(item => `${item[0]}`)
  let countries = [...new Set(_countries)];
  const _categories = _items.filter(item => item[0] === countries[0]).map(item => `${item[1]}`)
  console.log(countries)
  const _datasets = countries.map((country, index) => {
    return {
      label: country,
      data: _items.filter(item => item[0] === country).map(item => `${item[2]}`),
      borderColor: CHART_COLORS_LIST[index],
      backgroundColor: CHART_COLORS_LIST[index],
      yAxisID: country,
    }
  })
  console.log(_datasets)

  const data = {
    labels: _categories,
    datasets: [
      {
        label: countries[0],
        data: _items.filter(item => item[0] === countries[0]).map(item => `${item[2]}`),
        backgroundColor: CHART_COLORS_LIST,
      }
    ]
  };
  const config = {
    type: 'pie',
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: chartTitle
        }
      }
    },
  };
  const chart = new Chart(
    document.getElementById(chartId),
    config
  );
}

const createChart = (chartId, chartTitle, chartData) => {
  const _items = chartData.items
  const _countries = _items.map(item => `${item[0]}`)
  let countries = [...new Set(_countries)];
  const _categories = _items.filter(item => item[0] === countries[0]).map(item => `${item[1]}`)
  console.log(countries)
  const _datasets = countries.map((country, index) => {
    return {
      label: country,
      data: _items.filter(item => item[0] === country).map(item => `${item[2]}`),
      borderColor: CHART_COLORS_LIST[index],
      backgroundColor: CHART_COLORS_LIST[index],
      yAxisID: country,
    }
  })
  console.log(_datasets)
  
  const data = {
    labels: _categories,
    datasets: _datasets
  };
  const config = {
    type: 'line',
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,

      stacked: false,
      plugins: {
        title: {
          display: true,
          text: chartTitle
        }
      },
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',

          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
      }
    },
  };
  const chart = new Chart(
    document.getElementById(chartId),
    config
  );
}