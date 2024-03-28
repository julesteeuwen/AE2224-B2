import { LineChart } from "@mui/x-charts";
import { useEffect, useState } from "react";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

export interface Root {
	[key: string]: Data;
}

export interface Data {
	YEAR: {[key: number]: number;};
	MONTH_NUM: {[key: number]: number;};
	MONTH_MON: {[key: number]: string;};
	ENTITY_NAME: {[key: number]: string;};
	ENTITY_TYPE: {[key: number]: string;};
	CPLX_FLIGHT_HRS: {[key: number]: number;};
	CPLX_INTER: {[key: number]: number;};
	VERTICAL_INTER_HRS: {[key: number]: number;};
	HORIZ_INTER_HRS: {[key: number]: number;};
	SPEED_INTER_HRS: {[key: number]: number;};
	BADA_VERSION: {[key: number]: number;};
	[key: string]: any;
  }

  
const darkTheme = createTheme({
palette: {
	mode: 'dark',
},
});

const dateFormatter = (date: string) => {
	var formatted = new Date(parseInt(date))
	return formatted.toLocaleDateString()
};

export const ANSPChart = (props: {ansps: Array<string>}) => {

	// Fetch Data
	// const [datalist, setDatalist] = useState<Array<Root>>([]);
	const [data, setData] = useState<Root | null>(null);
	const ansp0 = props.ansps[0]
	useEffect(() => {
		fetch('http://localhost:5000/ansps/' + props.ansps.join(','))
			.then(response => response.json())
			.then((data: Root) => {
				// for(const key of Object.keys(data)) {
				// 	const newObj = Object.fromEntries(
				// 		Object.entries(data[key]).map(([k, v]) => {
				// 			var i = parseInt(k)
				// 			return [new Date(i), v]
				// 		})
				// 	  );
				// 	data[key] = newObj
	
				// }
				setData(data)
				console.log(data)

			})
			.catch((err) => {
				// Log error messages
				console.log(err.message);
			});
			
		},[props.ansps	]);	

	

	return (
		<ThemeProvider theme={darkTheme}>
			<h1 className="text-xl font-bold text-center">Graph</h1>
			<CssBaseline />
			<LineChart
				xAxis={ data ? [{ data: Object.keys(data[ansp0]?.CPLX_INTER || []), scaleType: 'utc' , valueFormatter: dateFormatter}] : [{data:[], scaleType: 'utc', valueFormatter: dateFormatter}] }
				series={props.ansps.map((ansp) => (
					{
					data: data ? Object.values(data[ansp]?.CPLX_INTER || []) : [],
					showMark: false,
					label: ansp,
					}
				))}
				width={1000}
				height={600}
			/>
		</ThemeProvider>

	);
};
