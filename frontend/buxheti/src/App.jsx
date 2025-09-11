import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Layout from "./pages/Layout";
import Register from "./pages/register";
import Home from './pages/home';






const App = () => {
 return(
    <BrowserRouter>
    <Routes>
        <Route path='/' element={<Layout/>}/>
        <Route index element={<Home/>}/>
        <Route path='register' element={<Register/>}/>
    </Routes>
    
    </BrowserRouter>
 )
};

export default App;

