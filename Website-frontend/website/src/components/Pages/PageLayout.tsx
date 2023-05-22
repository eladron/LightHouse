import React from 'react';
import '../../App.css';
import { MenuPage } from './MenuPage/MenuPage';


export interface PageLayoutProps {
    page: number;
    changePage(newPage: number): void;
}
export const PageLayout: React.FC<PageLayoutProps> = ({
    page, changePage,
}) => {

    switch (page) {
        case 0:
            return <MenuPage changePage={changePage}/>
        case 1:
            return null;
        default:
            return null;

    }
}
