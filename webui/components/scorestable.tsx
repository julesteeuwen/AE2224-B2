import { useEffect, useState } from "react";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { DataGrid } from "@mui/x-data-grid";
import { GridColDef } from "@mui/x-data-grid";
import Box from "@mui/material/Box";

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
    Complexity_score: {[key: number]: number;};
    Adjusted_density: {[key: number]: number;};
    Vertical_score: {[key: number]: number;};
    Horizontal_score: {[key: number]: number;};
    Speed_score: {[key: number]: number;};
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

export const ScoresTable = (props: {ansps: Array<string>}) => {

	// Fetch Data
	// const [datalist, setDatalist] = useState<Array<Root>>([]);
	const [data, setData] = useState<Root | null>(null);
	const ansp0 = props.ansps[0]
	useEffect(() => {
		fetch('http://localhost:5000/scores/daily/' + props.ansps.join(','))
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
    
    // const columns: GridColDef<(typeof rows)[number]>[] = Object.keys(data || {}).map((key) => {
    //     return {
    //         field: 'ansp',
    //         headerName: 'ANSP',
    //     };
    // });
    const firstItem = data ? data[Object.keys(data)[0]] : null;
    const columns: GridColDef<(typeof rows)[number]>[] = [
        {
            field: 'id', headerName: 'ID', width: 90
        },
        {
            field: 'ansp',
            headerName: 'ANSP',
            width: 100
        },
        {
            field: 'Date',
            headerName: 'Date',
            width: 100
        },
        {
            field: 'Adjusted_density',
            headerName: 'Adjusted Density',
            width: 150
        },
        {
            field: 'Horizontal_score',
            headerName: 'Horizontal Score',
            width: 150
        },
        {
            field: 'Vertical_score',
            headerName: 'Vertical Score',
            width: 150
        },
        {
            field: 'Speed_score',
            headerName: 'Speed Score',
            width: 150
        },
        {
            field: 'Complexity_score',
            headerName: 'Complexity Score',
            width: 150
        }
    ];
    var id = 0
    const rows = Object.keys(data || {}).map((key) => {
        var ansp_data = data ? data[key] : null;
        if (ansp_data) {
            Object.keys(ansp_data).map((id) => {
                return {
                    id: id,
                    ansp: key,
                    Date: dateFormatter(id),
                    Adjusted_density: ansp_data![id].Adjusted_density,
                    Horizontal_score: ansp_data![id].Horizontal_score,
                    Vertical_score: ansp_data![id].Vertical_score,
                    Speed_score: ansp_data![id].Speed_score,
                    Complexity_score: ansp_data![id].Complexity_score
                };
            });
        }
        return [];
    }).flat();
          
	return (
		<ThemeProvider theme={darkTheme}>
			<h1 className="text-xl font-bold text-center">Graph</h1>
			<CssBaseline />
            <Box sx={{ height: 400, width: '100%' }}>
                <DataGrid
                rows={rows ? rows : []}
                columns={columns}
                initialState={{
                    pagination: {
                    paginationModel: {
                        pageSize: 5,
                    },
                    },
                }}
                pageSizeOptions={[5]}
                checkboxSelection
                disableRowSelectionOnClick
                />
            </Box>
		</ThemeProvider>

	);
};
