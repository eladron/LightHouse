import React from 'react';
import { Table, TableBody, TableCell, Typography, TableHead, TableRow, Paper } from '@mui/material';
import { placements } from '../../utils';

export interface ResultPageProps {
    changePage(newPage: number): void;
}
export const ResultPage: React.FC<ResultPageProps> = ({
    changePage,
}) => {

    const sortedPlacements = Object.entries(placements).sort(([, a], [, b]) => a.worker - b.worker);

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'center' }}>
                <Table style={{ width: '20%', marginTop: '30px' }}>
                    <TableHead>
                        <TableRow>
                            <TableCell align="center"><b>תחנה</b></TableCell>
                            <TableCell align="center"><b>עובד</b></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {sortedPlacements.map(([id, placement]) => (
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
            <Typography variant="subtitle1" style={{ marginRight: '20px', textAlign: 'center' }}>
                ☻
            </Typography>
        </div>
    );
}

