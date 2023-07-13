import React from 'react';
import { Table, TableBody, TableCell, Typography, TableHead, TableRow } from '@mui/material';
import facturyImage from '../../Factury.png';


export interface ResultPageProps {
    changePage(newPage: number): void;
}
export const ResultPage: React.FC<ResultPageProps> = ({
    changePage,
}) => {
    
    const sortedPlacements = Object.entries(global.placements).sort(([, a], [, b]) => a.worker - b.worker);
    const placements = Object.entries(global.placements);
    const numRows = sortedPlacements.length;
    const midpoint = Math.ceil(numRows / 2);
    const rightRows = sortedPlacements.slice(midpoint);
    const centerRows = sortedPlacements.slice(0, midpoint);
    const placement_from_left = ['25.7%', '31.5%', '37.3%', '43%']
    const placement_from_top = ['17.5%', '33.5%', '36.5%', '52.5%','55.5%']

    console.log(global.revenue);

    const get_index_in_top = (index: number) => {
        if (index < 5) {
            return 0;
        }
        else if (index < 9) {
            return 1;
        }
        else if (index < 13) {
            return 2;
        }
        else if (index < 17) {
            return 3;
        }
        return 4;
    }

    const get_color_for_type = (type: string) => {
        if (type == 'screw') {
            return 'lightblue';
        }
        else if (type == 'water') {
            return 'lightgreen';
        }
        else if (type == 'piston') {
            return 'red';
        }
        else {
            return 'orange';
        }
    }

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'right', marginRight: '200px' }}>         
                <div style={{ display: 'inline-block', marginRight:'300px', marginTop:'50px'}}>
                    <img src={facturyImage} alt="Background Image" style={{ width: '120%', height: 'auto' }} />
                    {placements.map(([placementKey, placementValue]) => (
                        <div style={{ position: 'absolute', top: placement_from_top[get_index_in_top(Number(placementKey))], left: placement_from_left[(Number(placementKey)-1)%4], transform: 'translate(-50%, -50%)', textAlign: 'center' }}>
                            <p style={{ fontSize: '24px', color: 'black', backgroundColor: get_color_for_type(placementValue.station)  }}>{placementValue.worker} עובד</p>
                        </div>
                        ))}
                </div>
                <div style={{ display: 'inline-block' }}>
                <Table style={{ width: '130%', marginTop: '50px', fontSize: '20px'}}>
                        <TableHead>
                            <TableRow>
                                <TableCell align="center" style={{fontSize: '20px'}}><b>סוג תחנה</b></TableCell>
                                <TableCell align="center" style={{fontSize: '20px'}}><b>עובד</b></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {rightRows.map(([id, placement]) => (
                                <TableRow key={id}>
                                    <TableCell align="center" style={{fontSize: '20px'}}>{placement.station === "screw" ?
                                        "ברגים" : placement.station === "water" ? "עמדת מים" :
                                            placement.station === "piston" ? "בוכנה" :
                                                "ידית"}</TableCell>
                                    <TableCell align="center" style={{fontSize: '20px'}}>{placement.worker}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </div>
                <div style={{marginRight: '20px'}}>
                </div>
                <div style={{ display: 'inline-block'}}>
                <Table style={{ width: '130%', marginTop: '50px', fontSize: '50px' }}>
                        <TableHead>
                            <TableRow>
                                <TableCell align="center" style={{fontSize: '20px'}}><b>סוג תחנה</b></TableCell>
                                <TableCell align="center" style={{fontSize: '20px'}}><b>עובד</b></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {centerRows.map(([id, placement]) => (
                                <TableRow key={id}>
                                    <TableCell align="center" style={{fontSize: '20px'}}>{placement.station === "screw" ?
                                        "ברגים" : placement.station === "water" ? "עמדת מים" :
                                            placement.station === "piston" ? "בוכנה" :
                                                "ידית"}</TableCell >
                                    <TableCell align="center" style={{fontSize: '20px'}}>{placement.worker}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </div>
            </div>
            <div style={{ display: 'flex', marginBottom: '20px', justifyContent: 'Center' }}>
                <div style={{ display: 'inline-block', marginBottom: '20px', justifyContent: 'Center' }}>
                    <div style={{ backgroundColor: 'red', width: '20px', height: '20px', marginRight: '5px', marginTop: '8px' }}></div>
                </div>
                <div style={{ display: 'inline-block', marginBottom: '20px', justifyContent: 'Center' , marginRight:'15px'}}>
                    <Typography variant="body1" fontSize="25px" fontWeight="bold">
                        :בוכנה
                    </Typography>
                </div>
                <div style={{ display: 'inline-block', marginBottom: '20px', justifyContent: 'Center' }}>
                    <div style={{ backgroundColor: 'orange', width: '20px', height: '20px', marginRight: '5px', marginTop: '8px' }}></div>
                </div>
                <div style={{ display: 'inline-block', marginBottom: '20px', justifyContent: 'Center' , marginRight:'15px'}}>
                    <Typography variant="body1" fontSize="25px" fontWeight="bold">
                        :ידית ישר
                    </Typography>
                </div>
                <div style={{ display: 'inline-block', marginBottom: '20px', justifyContent: 'Center' }}>
                    <div style={{ backgroundColor: 'lightgreen', width: '20px', height: '20px', marginRight: '5px', marginTop: '8px' }}></div>
                </div>
                <div style={{ display: 'inline-block', marginBottom: '20px', justifyContent: 'Center' , marginRight:'15px'}}>
                    <Typography variant="body1" fontSize="25px" fontWeight="bold">
                        :עמדת מים
                    </Typography>
                </div>
                <div style={{ display: 'inline-block', marginBottom: '20px', justifyContent: 'Center' }}>
                    <div style={{ backgroundColor: 'lightblue', width: '20px', height: '20px', marginRight: '5px', marginTop: '8px' }}></div>
                </div>
                <div style={{ display: 'inline-block', marginBottom: '20px', justifyContent: 'Center' , marginRight:'15px'}}>
                    <Typography variant="body1" fontSize="25px" fontWeight="bold">
                        :ברגים
                    </Typography>
                </div>
            </div>
            <div style={{ display: 'flex', marginBottom: '20px' ,justifyContent:"Center"}}>
                <Typography variant="body1" fontSize='25px' fontWeight='bold'>
                    רווח צפוי: {global.revenue.toString()} ש"ח  || כמות בוכנה צפויה: {global.product_piston.toString()} || כמות ידית ישר צפויה: {global.product_handle.toString()} || כמות בדיקות מים צפויה: {global.product_water.toString()} || כמות ברגים צפויה: {global.product_screws.toString()}  
                </Typography>
            </div>
        </div>
    );
}
