import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import Button from '@mui/material/Button';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
//import axios from 'axios';

export interface MenuPageProps {
    changePage(newPage: number): void;
}
export const MenuPage: React.FC<MenuPageProps> = ({
    changePage,
}) => {

    const [tableValues, setTableValues] = React.useState<Array<Array<number>>>([
        // Row 1
        [0, 0, 0, 0, 0],
        // Row 2
        [0, 0, 0, 0, 0],
    ]);

    const [hours, setHours] = React.useState<number>(0);
    const [selectedFile, setSelectedFile] = React.useState(null);

    const handleValueChange = (rowIndex: number, colIndex: number, value: String) => {
        // Create a copy of the current tableValues array
        const updatedTableValues = [...tableValues];
        // Update the value at the specified row and column index
        updatedTableValues[rowIndex][colIndex] = Number(value);
        // Update the state with the new tableValues
        setTableValues(updatedTableValues);
    };

    const handleHoursChange = (value: String) => {
        setHours(Number(value));
    };

    const handleFileChange = (event:any) => {
        const file = event.target.files[0];
        setSelectedFile(file);
    };

    const handleSubmit = (event:any) => {
        
    };

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'center' }}>
                <Table style={{ width: '70%' }}>
                    <TableHead>
                        <TableRow>
                            <TableCell align='center'>
                                <Typography variant="subtitle1" fontWeight="bold">
                                    ברגים
                                </Typography>
                            </TableCell>
                            <TableCell align='center'>
                                <Typography variant="subtitle1" fontWeight="bold">
                                    בדיקות רטובות
                                </Typography>
                            </TableCell>
                            <TableCell align='center'>
                                <Typography variant="subtitle1" fontWeight="bold">
                                    בוכנה
                                </Typography>
                            </TableCell>
                            <TableCell align='center'>
                                <Typography variant="subtitle1" fontWeight="bold">
                                    ידית ישר
                                </Typography>
                            </TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {[1, 2].map((row, rowIndex) => (
                            <TableRow key={rowIndex}>
                                {[1, 2, 3, 4, 5].map((col, colIndex) => (
                                    <TableCell key={colIndex}>
                                        {colIndex === 4 && rowIndex === 0 ? (
                                            <b>כמות יחידות נדרשת</b>) :
                                            colIndex === 4 && rowIndex === 1 ? (
                                                <b>כמות יחידות במלאי</b>) :
                                                (
                                                    <TextField defaultValue="0" variant="outlined"
                                                        inputProps={{ style: { textAlign: 'center' } }}
                                                        onChange={(e) =>
                                                            handleValueChange(rowIndex, colIndex, e.target.value)} />
                                                )}
                                    </TableCell>
                                ))}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '70px' }}>
                <div style={{ display: 'grid', gridTemplateColumns: 'auto', gap: '20px', marginRight: '80px' }}>
                    <div style={{ display: 'grid', gridTemplateColumns: 'max-content auto', alignItems: 'center' }}>
                        <TextField defaultValue="8" variant="outlined" style={{ marginRight: '20px' }} inputProps={{ style: { textAlign: 'center' } }}
                            onChange={(e) => { handleHoursChange(e.target.value) }} />
                        <Typography variant="subtitle1" style={{ marginRight: '20px', textAlign: 'right' }}>
                            :הכנס מספר שעות עבודה
                        </Typography>
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'max-content auto', alignItems: 'center' }}>
                        <Button variant="contained" component="label">
                            העלה קובץ
                            <input type="file" style={{ display: 'none' }}
                                accept="application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                onChange={handleFileChange} />
                        </Button>
                        <Typography variant="subtitle1" style={{ marginRight: '20px', textAlign: 'right' }}>
                            :העלה קובץ אקסל
                        </Typography>
                    </div>
                </div>
            </div>
            <div style={{ display: 'flex', justifyContent: 'center', marginTop: '50px' }}>
                <Button variant="contained" color="primary" size="large"
                    style={{ fontSize: '1.5rem', padding: '16px 32px', minWidth: '240px' }}>
                    הרץ אלגוריתם
                </Button>
            </div>
        </div>
    );
}
