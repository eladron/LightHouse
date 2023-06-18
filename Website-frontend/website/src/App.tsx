import React from 'react';
import './App.css';
import { Header } from './components/AppHeader/Header';
import { PageLayout } from './components/Pages/PageLayout';

function App() {

    const [page, setPage] = React.useState<number>(0);


    const changePage = (newPage: number) => {
        setPage(newPage);
    }

    return (
        <div className="root">
            <Header page={page} changePage={changePage}/>
            <PageLayout page={page} changePage={changePage} />
        </div>
    );
}

export default App;
