import { endOfDay, startOfDay } from 'date-fns';
import { cssvar } from '@/util/layout';

export function parseAnnotations(annotations, data) {
  let chartAnnotations = [];

  const now = new Date();

  annotations.forEach((type) => {
    if (typeof type === 'number') {
      chartAnnotations.push({
        yAxis: type,
        lineStyle: { type: 'solid' },
      });
    }
    if (type === 'now') {
      chartAnnotations.push({
        xAxis: now,
        lineStyle: { type: 'solid' },
      });
    }
    if (type === 'startOfDay') {
      chartAnnotations.push({
        xAxis: startOfDay(now),
        lineStyle: { type: 'dotted' },
      });
    }
    if (type === 'endOfDay') {
      chartAnnotations.push({
        xAxis: endOfDay(now),
        lineStyle: { type: 'dotted' },
      });
    }
    if (type === 'average') {
      const sum = data.map((p) => p[1]).reduce((a, b) => a + b);
      const avg = sum / data.length;

      chartAnnotations.push({
        yAxis: avg,
        lineStyle: { type: 'dotted' },
      });
    }
  });

  return chartAnnotations;
}

export const DEFAULT_LABEL_STYLE = {
  position: 'inside',
  height: 22,
  color: cssvar('--color-white-rgb'),
  fontFamily: 'Roboto',
  fontWeight: 'bolder',
  fontSize: 13,
  lineHeight: 20,
  align: 'center',
  verticalAlign: 'middle',
  backgroundColor: cssvar('--color-lighter-rgb'),
  padding: [0, 6, 0, 6],
  borderRadius: 4,
};
