import React from 'react';
import {Link, Routes, Route} from 'react-router-dom'
import './App.css';
import Login from './components/Login';
import Search from './components/Search';
import DocumentComplete from './components/DocumentComplete'
import Register from './components/Register';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />}></Route>
      <Route path="/search" element={<Search />}></Route>
      <Route path="/register" element={<Register />}></Route>
      <Route path="/result/*" element={<DocumentComplete />}></Route>
    </Routes>
  );
}

export default App;
