import '../../App.css';
import { pages, API_URL } from '../../utils';
import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import IconButton from '@mui/material/IconButton';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
//import axios from 'axios';

export interface HeaderProps {
    page: number;
    changePage(newPage: number): void;
}
export const Header: React.FC<HeaderProps> = ({
    page, changePage
}) => {

    const handleBackButtonClick = () => {
        changePage(0);
    };

    return (
        <AppBar position="sticky" color="primary">
            <Container maxWidth="xl">
                <Toolbar disableGutters sx={{ display: 'flex' }}>
                    { page === 1 ?
                    <IconButton
                        edge="start"
                        color="inherit"
                        aria-label="back"
                        onClick={() => handleBackButtonClick()}
                    >
                        <ArrowBackIcon />
                    </IconButton> : null}
                    <Typography
                        variant="h3"
                        sx={{
                            marginLeft: 'auto',
                            marginRight: '20px',
                            display: { xs: 'none', md: 'flex' },
                            fontWeight: 700,
                            color: 'inherit',
                        }}>
                        {pages[page]}
                    </Typography>
                </Toolbar>
            </Container>
        </AppBar>
    );
}
