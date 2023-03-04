import _merge from 'lodash/merge';
import {
  Chart as ChartJS,
  Filler,
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import annotationPlugin from 'chartjs-plugin-annotation';

export function useChart(chartOptions) {
  ChartJS.register(
    Filler,
    CategoryScale,
    LinearScale,
    TimeScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    ChartDataLabels,
    annotationPlugin
  );

  // https://jhildenbiddle.github.io/mergician
  const options = _merge(
    {
      responsive: true,
      maintainAspectRatio: false,
      // layout: {
      //   padding: {
      //     left: -50,
      //   },
      // },
      plugins: {
        // https://chartjs-plugin-datalabels.netlify.app/guide/options.html
        datalabels: {
          color: '#FFF',
          backgroundColor: '#767676',
          // borderColor: '#333',
          borderRadius: 3,
          padding: { top: 3, bottom: 0, left: 3, right: 3 },
          font: {
            weight: 'bold',
          },
        },
      },
      scales: {
        x: {
          type: 'time',
          time: {
            displayFormats: {
              minute: 'HH:MM',
              hour: 'HH',
            },
          },
          grid: { display: false },
          ticks: {
            display: true,
            color: '#333333',
            font: {
              family: 'Roboto',
              weight: 500,
            },
          },
          border: { display: false },
        },
        y: {
          grid: { display: false },
          ticks: { display: false },
          border: { display: false },
        },
      },
    },
    chartOptions
  );

  return { options };
}
