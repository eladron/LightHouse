import React from 'react';
import { Table, TableBody, TableCell, Typography, TableHead, TableRow } from '@mui/material';

export interface ResultPageProps {
    changePage(newPage: number): void;
}
export const ResultPage: React.FC<ResultPageProps> = ({
    changePage,
}) => {
    
    const sortedPlacements = Object.entries(global.placements).sort(([, a], [, b]) => a.worker - b.worker);
    const numRows = sortedPlacements.length;
    const midpoint = Math.ceil(numRows / 2);
    const rightRows = sortedPlacements.slice(midpoint);
    const centerRows = sortedPlacements.slice(0, midpoint);


    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'right', marginRight: '200px' }}>
                <div style={{ display: 'inline-block' }}>
                <Table style={{ width: '130%', marginTop: '50px', fontSize: '18px'}}>
                        <TableHead>
                            <TableRow>
                                <TableCell align="center"><b>סוג תחנה</b></TableCell>
                                <TableCell align="center"><b>עובד</b></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {rightRows.map(([id, placement]) => (
                                <TableRow key={id}>
                                    <TableCell align="center">{placement.station === "screw" ?
                                        "ברגים" : placement.station === "water" ? "עמדת מים" :
                                            placement.station === "piston" ? "בוכנה" :
                                                "ידית"}</TableCell>
                                    <TableCell align="center">{placement.worker}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </div>
                <div style={{ display: 'inline-block'}}>
                <Table style={{ width: '130%', marginTop: '50px', fontSize: '18px' }}>
                        <TableHead>
                            <TableRow>
                                <TableCell align="center"><b>סוג תחנה</b></TableCell>
                                <TableCell align="center"><b>עובד</b></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {centerRows.map(([id, placement]) => (
                                <TableRow key={id}>
                                    <TableCell align="center">{placement.station === "screw" ?
                                        "ברגים" : placement.station === "water" ? "עמדת מים" :
                                            placement.station === "piston" ? "בוכנה" :
                                                "ידית"}</TableCell>
                                    <TableCell align="center">{placement.worker}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
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
